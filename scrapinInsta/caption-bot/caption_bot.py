from selenium import webdriver
from os.path import isfile, join, abspath
from os import listdir
import time

def load_img_paths():
    img_paths = []
    files = [f for f in listdir('../data/media/') if isfile(join('../data/media/', f))]
    for file in files:
        if file.endswith('.jpg'):
            name = abspath('../data/media/' + file)
            img_paths.append(name)

    return img_paths


def write_to_file(path, text):
    id = path.split('\\')[-1].split('.')[0]
    if text.lower().startswith('i think it\'s '):
        text = text[13:]
    elif text.lower().startswith('i am not really confident, but i think it\'s '):
        text = text[45:]
    elif text.lower().startswith('i can\'t really describe the picture') or text.lower().startswith('i think this may be inappropriate content'):
        text = ''

    print(id + ' --- ' + text)
    if text != '':
        file = open('generated-captions.txt', 'a+', encoding='utf-8')
        file.write(id + '|' + text + '\n')
        file.close()


def upload_img(driver, paths):
    for path in paths[1290:]:
        driver.find_element_by_id('idImageUploadField').send_keys(path)
        driver.implicitly_wait(10)
        text = driver.find_element_by_id('captionLabel')
        while text.text == 'Uploading image ...' or text.text == 'Analyzing image ...' or text.text == 'Optimizing image ...':
            time.sleep(3)

        print(text.text)
        write_to_file(path, text.text)


if __name__ == '__main__':
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get('https://www.captionbot.ai/')
    paths = load_img_paths()
    upload_img(driver, paths)