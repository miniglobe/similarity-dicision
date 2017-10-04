# -*- coding: utf-8 -*-

import tensorflow as tf
from models import input_data


tf.app.flags.DEFINE_integer('batch_size', 32, """バッチサイズ""")

FLAGS = tf.app.flags.FLAGS


def main():
  data = input_data.get_batch(FLAGS.batch_size)


if __name__ == '__main__':
  main()