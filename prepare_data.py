import csv
import os


def get_files(path):
    return [path.split('.')[0] for path in os.listdir(path)]


def make_files(img_dir, txt_dir):
    images_name = []
    captions = []

    with open(txt_dir) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for row in csvReader:
            print(row)
            images_name.append(row[0])
            captions.append(row[1])

    for i, image_name in enumerate(images_name):
        with open(os.path.join('ig_data/texts',image_name+'.txt'), 'a') as file:
            file.write(captions[i])


def delete(img_dir, txt_dir):

    images = get_files(img_dir)
    captions = get_files(txt_dir)

    captions_to_delete = []
    images_to_delete = []
    for caption in captions:
        if caption not in images:
            captions_to_delete.append(str(caption+'.txt'))
    for image in images:
        if image not in captions:
            print(image)
            images_to_delete.append(str(image+'.jpg'))

    print(len(images_to_delete), len(captions_to_delete))

    [os.remove('ig_data/images/'+str(image_name)) for image_name in images_to_delete]
    [os.remove('ig_data/texts/'+str(txt_name)) for txt_name in captions_to_delete]

    captions_0 = get_files(img_dir)
    images_0 = get_files(txt_dir)

    if len(captions_0) == len(images_0):
        print("successfully deleted")
    else:
        print("something went wrong")


#make_files('', 'ig_data/captions3.csv')
delete('ig_data/images', 'ig_data/texts')