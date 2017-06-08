#coding=utf-8
#tensorflow高效数据读取训练
import tensorflow as tf
import cv2
import numpy as np
import os
from PIL import Image
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import sys, getopt

from imagenet_data import ImagenetData

FLAGS = tf.app.flags.FLAGS

tf.app.flags.DEFINE_string('subset', 'train', 'Either "train" or "validation".')
tf.app.flags.DEFINE_string('type', 'change', '')
tf.app.flags.DEFINE_string('input', '02_31.mp4', '02_31.mp4')
# tf.app.flags.DEFINE_string('datadir', '', 'some.mp4')
# pre data_dir
# tf.app.flags.DEFINE_string('datadir', '', '')
# tf.app.flags.DEFINE_string('subset', 'train', '')



# opts, args = getopt.getopt(sys.argv[1:], "hi:o:t:d:")
input_file=FLAGS.input
output_file=""
type=FLAGS.type

print("input_file")
print(input_file)
print("type")
print(type)

# data_file=""
# for op, value in opts:
#     if op == "-i":
#         input_file = value
#     elif op == "-o":
#         output_file = value
#     elif op == "-t":
#         type = value
#     elif op == "-d":
#         data_file = value

def decode_jpeg(image_buffer, scope=None):
  """Decode a JPEG string into one 3-D float image Tensor.

  Args:
    image_buffer: scalar string Tensor.
    scope: Optional scope for name_scope.
  Returns:
    3-D float Tensor with values ranging from [0, 1).
  """
  with tf.name_scope(values=[image_buffer], name=scope,
                     default_name='decode_jpeg'):
    # Decode the string as an RGB JPEG.
    # Note that the resulting image contains an unknown height and width
    # that is set dynamically by decode_jpeg. In other words, the height
    # and width of image is unknown at compile-time.
    image = tf.image.decode_jpeg(image_buffer, channels=3)

    # After this point, all image pixels reside in [0,1)
    # until the very end, when they're rescaled to (-1, 1).  The various
    # adjust_* ops all require this range for dtype float.
    image = tf.image.convert_image_dtype(image, dtype=tf.float32)
    return image
    
def _int64_feature(value):
  """Wrapper for inserting int64 features into Example proto."""
  if not isinstance(value, list):
    value = [value]
  return tf.train.Feature(int64_list=tf.train.Int64List(value=value))


def _bytes_feature(value):
  """Wrapper for inserting bytes features into Example proto."""
  return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

def _int64_():
  return tf.FixedLenFeature([], tf.int64)


def _bytes_():
  return tf.FixedLenFeature([], tf.string)


def read_and_decode(filename_queue):
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)

    # print("serialized_example")
    # print(serialized_example.shape)

    features = tf.parse_single_example(
        serialized_example,
        features={
        'image/height': _int64_(),
        'image/width': _int64_(),
        'image/colorspace': _bytes_(),
        'image/channels': _int64_(),
        'image/class/label': _int64_(),
        'image/class/text': _bytes_(),
        'image/format': _bytes_(),
        'image/filename': _bytes_(),
        'image/encoded': _bytes_()
        })
    # image = tf.decode_raw(features['image/encoded'], tf.uint8)

    # label = tf.cast(features['image/class/label'], tf.int64)
    height = tf.cast(features['image/height'], tf.int64)
    width = tf.cast(features['image/width'], tf.int64)
    text = tf.cast(features['image/class/text'], tf.string)
    filename = tf.cast(features['image/filename'], tf.string)
    # depth = tf.cast(features['image/channels'], tf.int64)
    # return image, label, height, width, depth
    return decode_jpeg(features['image/encoded']), height, width, text, filename
def save(dirname, filename, filedata):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    plt.imsave(dirname+"/"+filename, filedata)
    print("save ",dirname+"/"+filename,"   ok!")

def get_all_records(dataset):
    print("len dataset.data_files():")
    print(len(dataset.data_files()))
    print("dataset.num_examples_per_epoch():")
    print(dataset.num_examples_per_epoch())
    FILE = dataset.data_files()
    with tf.Session() as sess:
        # coder = ImageCoder()
        for f in FILE:
    
            filename_queue = tf.train.string_input_producer([ f ])
            image, height, width, text, filename = read_and_decode(filename_queue)
                
            init_op = tf.global_variables_initializer()
            sess.run(init_op)
            coord = tf.train.Coordinator()
            threads = tf.train.start_queue_runners(coord=coord)

            for i in range(dataset.num_examples_per_epoch()):
                img_data, h, w, t,fn = sess.run([image, height, width, text, filename])
                # print(img_data.shape)

                type_real=t.decode().split('_')[0]
                videofilename_base=os.path.basename(input_file).split('.')[0]
                if videofilename_base in fn.decode() :
                    filename_save=fn.decode()
                    if type != "" and type_real == type:
                        save(videofilename_base, filename_save, img_data)
                    elif type == "":
                        save(videofilename_base, filename_save, img_data)

        coord.request_stop()
        coord.join(threads)


#测试上面的压缩、解压代码
# def test():
#     dataset = ImagenetData(subset=FLAGS.subset)
#     print(dataset.data_files())
    
#     # encode_to_tfrecords("data/train.txt","data")
#     get_all_records(data_file)

# test()

def main(_):
#       dataset = ImagenetData(subset=FLAGS.subset)
#   assert dataset.data_files()
#   if tf.gfile.Exists(FLAGS.train_dir):
#     tf.gfile.DeleteRecursively(FLAGS.train_dir)
#   tf.gfile.MakeDirs(FLAGS.train_dir)
#   inception_train.train(dataset)
    dataset = ImagenetData(subset=FLAGS.subset)
    print(dataset.data_files())
    
    # encode_to_tfrecords("data/train.txt","data")
    get_all_records(dataset)


if __name__ == '__main__':
  tf.app.run()
