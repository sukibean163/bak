from colabtools import table, publish

import numpy as np

import google3

import tensorflow.google as tf


def EncodeImage(image_tensor):
  with tf.Session():
    image_encoded = tf.image.encode_png(tf.constant(image_tensor)).eval()
  return image_encoded


def Read(record_file):
  keys_to_features = {
    'view1/image/encoded': tf.FixedLenFeature(
        (), dtype=tf.string, default_value=''),
    'view1/image/format': tf.FixedLenFeature(
        [], dtype=tf.string, default_value='png'),
    'view1/image/height': tf.FixedLenFeature(
        [1], dtype=tf.int64, default_value=64),
    'view1/image/width': tf.FixedLenFeature(
        [1], dtype=tf.int64, default_value=64),
    'view2/image/encoded': tf.FixedLenFeature(
        (), dtype=tf.string, default_value=''),
    'view2/image/format': tf.FixedLenFeature(
        [], dtype=tf.string, default_value='png'),
    'view2/image/height': tf.FixedLenFeature(
        [1], dtype=tf.int64, default_value=64),
    'view2/image/width': tf.FixedLenFeature(
        [1], dtype=tf.int64, default_value=64),
    'image/encoded': tf.FixedLenFeature(
        [2], dtype=tf.string, default_value=['','']),
    'same_object': tf.FixedLenFeature(
        [1], dtype=tf.int64, default_value=-1),
    'relative_pos': tf.FixedLenFeature(
        [3], dtype=tf.float32),
  }
  with tf.Graph().as_default():            
    filename_queue = tf.train.string_input_producer([record_file], capacity=10)
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)
    example = tf.parse_single_example(
        serialized_example,
        keys_to_features)
    #png1 = example['view1/image/encoded']
    #png2 = example['view2/image/encoded']
    png = example['image/encoded']
    coord = tf.train.Coordinator()
    print 'Reading images:'
    with tf.Session() as sess:
      queue_threads = tf.start_queue_runners(sess=sess, coord=coord)
      #image1, image2 = sess.run([png1, png2])
      image1, image2 = sess.run([png[0], png[1]])
      publish.image(encoded_image=image1, width=20)
      publish.image(encoded_image=image2, width=20)
    coord.request_stop()
    coord.join(queue_threads)


image_tensor1 = np.random.randint(255, size=(4, 5, 3)).astype(np.uint8)
image_tensor2 = np.random.randint(255, size=(4, 5, 3)).astype(np.uint8)
png1 = EncodeImage(image_tensor1)
png2 = EncodeImage(image_tensor2)
publish.image(encoded_image=png1, width=20)
publish.image(encoded_image=png2, width=20)

# Note: for the png files, just use png1 = f1.read()


example = tf.Example(features=tf.Features(feature={
   'view1/image/encoded': tf.Feature(bytes_list=tf.BytesList(value=[png1])),
   'view1/image/height': tf.Feature(int64_list=tf.Int64List(value=[4])),
   'view1/image/width': tf.Feature(int64_list=tf.Int64List(value=[5])),
   'view1/image/format': tf.Feature(bytes_list=tf.BytesList(value=['png'])),
   'view2/image/encoded': tf.Feature(bytes_list=tf.BytesList(value=[png2])),
   'view2/image/height': tf.Feature(int64_list=tf.Int64List(value=[4])),
   'view2/image/width': tf.Feature(int64_list=tf.Int64List(value=[5])),
   'view2/image/format': tf.Feature(bytes_list=tf.BytesList(value=['png'])),
   'image/encoded': tf.Feature(bytes_list=tf.BytesList(value=[png1, png2])),
   'same_object': tf.Feature(int64_list=tf.Int64List(value=[1])),
   'relative_pos': tf.Feature(float_list=tf.FloatList(value=[1.2,0.4,-0.9]))}))

# print example

examples = [example]
output_file = '/tmp/data2.tfrecord'
with tf.python_io.TFRecordWriter(output_file) as writer:
  for record in examples:
    writer.write(record.SerializeToString())

Read(output_file)
