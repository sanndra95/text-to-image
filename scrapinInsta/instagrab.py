from string import ascii_letters, digits
from time import sleep
from bs4 import BeautifulSoup
from copy import copy
import requests
from utils import *
import csv
import urllib.request as urllib

# set the desired hashtag
the_item = "flower"
# set the number of photos you want to collect, instagram eill not allow you to collect all the posts at 
# once, so you will have to go several timer to collect the desired amount
max_scrape = 5000
insta_path = "explore/tags/"
prefix = "photos"
# Create folders as necessary
data_path = "data/data" + "_" + prefix + "_" + the_item
media_path = "data/media"

# set all the paths, driver, read configuration, load more, get the previous posts
create_folders()
the_posts = previous_posts()
deets = read_default_config()
driver, actionChains = set_up_driver()
some_element = load_more(driver)

# then press space over an over again for a while
how_many = 1000
overlap = set()
all_links = []

# why nine? there are 9 recurring top posts before you get into the recent posts
first_time = False
while len(all_links) < how_many:
    print("koliko sam do sada stavio %d" % len(all_links))
    
    # send a key stroke to the page to scroll down
    some_element = driver.find_element_by_tag_name("body")

    # scroll down for 10 times
    for i in range(25):
        some_element.send_keys(" ")
        sleep(0.5)

    # get the mini images, ones that are shown on the search page
    #img_class = some_element.find_elements_by_css_selector("img")
    #print("*** found img tags no: %d " % len(img_class))

    # get the postfix names that will be added to the page URL and then you will be able to loop through it and
    # to get into the certain post to get the real BIG image and all the hashtags that are added to it
    all_links.extend([u.find_element_by_css_selector('a').get_attribute("href").split('/')[4] for u in driver.find_elements_by_class_name("_bz0w")])

    # check if the posts on the page have already been scraped

    # do the intersection of two sets
    #   first - the_posts: data from /metadata.json, data about the previously downloaded posts
    #   second - all_links: new data to scrape
    # overlap will consists of elements that are in the first and the second set
    # if len of the overlap is 0 -> there's no elements in the second set that are in the first set in the same time
    overlap = set(the_posts.keys()).intersection(set(all_links))
    print("overlap:", len(overlap))

    # class doesn't exist anymore, should try to figure it out what the class was representing earlier
    #how_many = len(driver.find_elements_by_class_name("_icyx7"))


print("total : %d" % len(all_links))
print("total *unique: %d" % len(set(all_links)))


def write_in_temp(scraped_links):
    # print the number of links/codes found in the page and save the list in a temporary file in case everything breaks down.
    if not os.path.exists(data_path+"/temp_links.json"):
        os.makedirs(data_path+"/temp_links.json")
    f = open(data_path+"/temp_links.json","a")
    json.dump(scraped_links,f, separators=',\n')
    f.close()


# scrape post pages + download media objects (photos only along with the description and hashtags written by owner)

def fixit(ss):
    return "".join([s for s in ss if s in ascii_letters+digits]).lower()


def extract_hashtags(ss):
    """
        Extracts the hashtags from the image caption! DONE!
    :param ss:
    :return:
    """
    ss = ss.replace("\n"," ")
    plist = ss.split(" ")
    tags = list(p for p in plist if len(p)>0 and p[0]=="#")
    tt = []
    for t in tags:
        tt += t.split("#")
    return list(set(list(fixit(t) for t in tt if len(t)>0)))


# scrape new post pages + download media objects (photos or videos)
def scrape_single_code(a_code,sleeper=1):
    from ast import literal_eval
    good_stuff = None
    all_fine = True
    try:
        tt = requests.get("https://www.instagram.com/p/"+a_code,timeout=2)
        tt_soup = BeautifulSoup(tt.text, "lxml")
        sleeper = 1
    except:
        all_fine = False
        print("$",end="",flush=True)
        sleep(sleeper)
    
    if all_fine:
        # find all the javascript tags in the code
        all_texts = [u.get_text() for u in tt_soup.find_all("script")]

        # extract the one that starts with this particular string
        try:
            all_texts = [at for at in all_texts if "window._sharedData" in at[:50]][0]
        except Exception:
            return None
        # fix the JavaScript syntax so that it can be transformed to Python code
        all_texts = all_texts.replace("window._sharedData","")
        all_texts = all_texts.replace("true","True")
        all_texts = all_texts.replace("false","False")
        all_texts = all_texts.replace("null","None")
        

        # extract the dict from the code and reach for the good stuff
        stuff = literal_eval(all_texts[3:-1])
        try:
            good_stuff = copy(stuff["entry_data"]["PostPage"][0]['graphql']['shortcode_media'])
        except Exception:
            return None
        
        # add some extra to the dict
        #good_stuff["scrape_ts"] = str(datetime.now())[:19]

        # get the caption
        edges = good_stuff.get("edge_media_to_caption").get("edges")
        extracted_hashtags = []
        for edge in edges:
            node = edge["node"]
            text = node["text"].encode('utf-16','surrogatepass').decode('utf-16')
            extracted_hashtags.extend(extract_hashtags(text))

        good_stuff["caption_tags"] = extracted_hashtags
        # get the caption

        # get the accessibility caption
        try:
            good_stuff['caption'] = good_stuff['accessibility_caption']
        except:
            good_stuff['caption'] = '-33'
        
        if good_stuff["is_video"]:
            print("It is video")
            return None
        else:
            good_stuff["object_url"] = good_stuff["display_url"]
            good_stuff["the_fname"] = a_code + ".jpg"
        #print(".",end="",flush=True)
    return good_stuff


def download_image(url, a_code, downloaded):
    urllib.urlretrieve(url, 'data\\media\\' + str(a_code) + '.jpg')
    return downloaded + 1


# scrape post pages for many codes
def scrape_codes(some_codes):
    print("for scraping: %d" % len(some_codes))
    downloaded = 0
    new_stuff = {}
    sleeptime=1
    cc = 0

    scraped_codes = []
    for a_code in some_codes:
        cc += 1
        if cc % 50 == 0: print(len(new_stuff))
        new_stuff[a_code] = copy(scrape_single_code(a_code,sleeptime))

        if new_stuff[a_code] is not None:
            downloaded = download_image(new_stuff[a_code]['display_url'], a_code, downloaded)
            downloaded = downloaded
            print("downloaded for now: %d" % downloaded)

            hashtags = new_stuff[a_code]["caption_tags"]

            with open(os.path.join('data','media',str(a_code)+'.csv'), 'w+', newline='') as f:
                header = ['no', 'hashtag']
                writer = csv.DictWriter(f, fieldnames=header)
                writer.writeheader()
                for i, hashtag in enumerate(hashtags):
                    writer.writerow({'no' : str(i), 'hashtag' : str(hashtag)})

            with open(os.path.join('data','media',str(a_code)+'.txt'), 'w+') as f:
                f.write(new_stuff[a_code]['caption'].replace('Image may contain: ', ''))
            scraped_codes.append(a_code)

        if new_stuff[a_code]==None:
            del new_stuff[a_code]
            sleeptime += sleeptime
        else:
            sleeptime = 1

    return scraped_codes


# scrape new post pages (not the photo itself) and add to storage
scraped_codes = scrape_codes([u for u in set(all_links) if not u in the_posts])
print("Final scraped codes: %d " % len(scraped_codes))
scraped_codes = scraped_codes.extend(the_posts)
write_in_temp(scraped_codes)

# close the driver
driver.close()

