import os
import csv

target_img_dir = 'ig_data/images/'
target_txt_dir = 'ig_data/texts/'


def load_txt_data(img_list):
    data = {}

    with open('ig_data/captions.csv') as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        next(read_csv, None)
        for row in read_csv:
            if row[0] in img_list:
                data[row[0]] = row[1]

    return data


def load_img_names():
    return [path.split('.')[0] for path in os.listdir(target_img_dir)]


def create_txt_data(data):
    for k, v in data.items():
        file_name = target_txt_dir + k + '.txt'
        file = open(file_name, 'w+')
        file.write(v)
        file.close()


def delete_images(data, img_names):
    images_to_delete = []
    for name in img_names:
        if name not in data.keys():
            images_to_delete.append(name)

    print(len(images_to_delete))

    [os.remove(target_img_dir + str(image_name) + '.jpg') for image_name in images_to_delete]

def main():
    img_names = load_img_names()
    print(img_names)
    print(len(img_names))
    data = load_txt_data(img_names)
    print(data)
    print(len(data))
    #delete_images(data, img_names)
    create_txt_data(data)


if __name__ == '__main__':
    main()
