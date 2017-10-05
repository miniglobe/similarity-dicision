# -*- coding: utf-8 -*-

import tensorflow as tf
from models import input_data


tf.app.flags.DEFINE_integer('batch_size', 32, """バッチサイズ""")
FLAGS = tf.app.flags.FLAGS


def main():
  image, text = input_data.get_batch(FLAGS.batch_size)
  loss_op = loss(convolute_image(image), convolute_text(text, num_chars=2573))
  train_op = minimize(loss_op)
  with tf.Session() as sess:
    init_op = tf.global_variables_initializer()
    sess.run(init_op)
    for i in range(10000):
      _, loss_value = sess.run([train_op, loss_op])
      if i % 100 == 0:
        print('loss_value: %d' % (loss_value))


def convolute_image(image, training=True):
  with tf.variable_scope('conv1'):
    output = tf.layers.conv2d(image, 64, [5, 5], strides=(2, 2), padding='SAME')
    output = tf.nn.relu(tf.layers.batch_normalization(output, training=training), name='output')
  with tf.variable_scope('conv2'):
    output = tf.layers.conv2d(output, 128, [5, 5], strides=(2, 2), padding='SAME')
    output = tf.nn.relu(tf.layers.batch_normalization(output, training=training), name='output')
  with tf.variable_scope('conv3'):
    output = tf.layers.conv2d(output, 256, [5, 5], strides=(2, 2), padding='SAME')
    output = tf.nn.relu(tf.layers.batch_normalization(output, training=training), name='output')
  with tf.variable_scope('conv4'):
    output = tf.layers.conv2d(output, 512, [5, 5], strides=(2, 2), padding='SAME')
    output = tf.nn.relu(tf.layers.batch_normalization(output, training=training), name='outputs')
  with tf.variable_scope('fc1'):
    output = tf.contrib.layers.flatten(output)
    output = tf.layers.dense(output, 200)
    output = tf.nn.relu(output)
  with tf.variable_scope('fc2'):
    output = tf.layers.dense(output, 100)
    output = tf.nn.sigmoid(output)
  return output


def convolute_text(text, num_chars, training=True):
  w = tf.get_variable("embedding", [num_chars, 128])
  output = tf.gather(w, text)
  convs = []
  for filter_size in (2,3,4,5):
    conv = tf.layers.conv1d(output, 64, filter_size, 1, padding='SAME')
    conv = tf.nn.relu(conv)
    convs.append(conv)

  output = tf.concat(convs, axis=1)
  output = tf.contrib.layers.flatten(output)
  output = tf.layers.dense(output, 1024)
  output = tf.layers.batch_normalization(output, training=training)
  output = tf.layers.dense(output, 100)
  output = tf.nn.sigmoid(output)
  return output


def loss(d_image, d_text):
  loss = tf.reduce_mean(tf.square(d_image - d_text))
  return loss


def minimize(loss):
  return tf.train.AdamOptimizer().minimize(loss)


if __name__ == '__main__':
  main()