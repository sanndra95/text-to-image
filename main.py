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


img_dir_path = 'ig_data/images/'
txt_dir_path = 'ig_data/texts/'
model_dir_path = 'ig-models/'

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

#training
start_time = time.time()

logs = gan.fit(model_dir_path=model_dir_path, image_label_pairs=image_label_pairs,
        snapshot_dir_path=current_dir + '/ig_data/snapshots',
        snapshot_interval=10,
        batch_size=batch_size,
        epochs=epochs)

end_time = time.time()
print(end_time-start_time)


from training_plot import on_epoch_end

on_epoch_end(logs)


"""
#testing
from dcgan import DCGan

gan = DCGan()
gan.load_model(model_dir_path)
text = 'one black guitar on white backgound'
generated_image = gan.generate_image_from_text(text)
generated_image.save(current_dir + '/data/outputs/' + DCGan.model_name + '-generated-' + str(0) + '-' + str(0) + '.png')
"""