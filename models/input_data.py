# -*- coding: utf-8 -*-
import tensorflow as tf

def get_batch(batch_size):
  filename = './data/blog_data.tfrecord'
  filename_queue = tf.train.string_input_producer([filename], shuffle=True)
  reader = tf.TFRecordReader()
  _, seliarized_data = reader.read(filename_queue)
  features = tf.parse_single_example(seliarized_data, features={
    'image': tf.FixedLenFeature([], tf.string),
    'width': tf.FixedLenFeature([], tf.int64),
    'height': tf.FixedLenFeature([], tf.int64),
    'depth': tf.FixedLenFeature([], tf.int64),
    'text': tf.FixedLenFeature([5000], tf.int64)
  })


  image = tf.cast(tf.image.decode_png(features['image'], channels=3), tf.float32) / 255.0
  image = tf.image.resize_images(image, [128, 128])

  min_queue_examples = 10
  num_threads = 2
  images, text = tf.train.shuffle_batch(
        [image, features['text']],
        batch_size=batch_size,
        num_threads=num_threads,
        capacity=min_queue_examples + 3 * batch_size,
        min_after_dequeue=min_queue_examples)
  return images, text