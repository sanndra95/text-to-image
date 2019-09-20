from image_text_loader import load_normalized_img_and_text
import numpy as np
import os
import sys
from random import shuffle
import keras.backend.tensorflow_backend as KTF
import tensorflow as tf
import time

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)

KTF.set_session(sess)

seed = 42
np.random.seed(seed)

current_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(current_dir, '..'))
current_dir = current_dir if current_dir is not '' else '.'

data_folder = 'data'
img_dir_path = data_folder + '/images/'
txt_dir_path = data_folder + '/texts/'
model_dir_path = 'models/'
snapshots_dir_path = '/snapshots/'
output_dir_path = '/' + data_folder + '/outputs/'
mode = 'test'

img_width = 64
img_height = 64
img_channels = 3

from dcgan import DCGan

image_label_pairs = load_normalized_img_and_text(img_dir_path, txt_dir_path, img_width=img_width,
                                                     img_height=img_height)

shuffle(image_label_pairs)

gan = DCGan()
gan.img_width = img_width
gan.img_height = img_height
gan.img_channels = img_channels
gan.random_input_dim = 200
gan.glove_source_dir_path = './very_large_data'

batch_size = 5
epochs = 2000


if mode == 'train':
    #training
    start_time = time.time()

    logs = gan.fit(model_dir_path=model_dir_path, image_label_pairs=image_label_pairs,
            snapshot_dir_path=current_dir + snapshots_dir_path,
            snapshot_interval=10,
            batch_size=batch_size,
            epochs=epochs)

    from training_plot import on_epoch_end

    on_epoch_end(logs)

    end_time = time.time()
    print(end_time-start_time)
elif mode == 'test':
    #testing
    from dcgan import DCGan

    gan = DCGan()
    gan.load_model(model_dir_path)
    text = 'person holding black guitar'
    generated_image = gan.generate_image_from_text(text)
    generated_image.save(current_dir + output_dir_path + DCGan.model_name + '-generated-' + str(0) + '-' + str(0) + '.png')
else:
    print('Wrong mode string')
