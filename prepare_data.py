# -*- coding: utf-8 -*-

import tensorflow as tf
from google.cloud import datastore
import numpy as np
import urllib.request
from PIL import Image
import io

PROJECT_ID = "persian-172808"
DATA_STORE_KEY_PATH = "/home/vagrant/.json_keys/persian-3a9988725cae.json"
STORAGE_STORE_KEY_PATH = "/home/vagrant/.json_keys/persian-efe392f65854.json"
BUCKET_NAME = "persian-172808.appspot.com"
record_file = './data/blog_data.tfrecords'

params = {
  "thumnail_width": 180
  , "thumnail_height": 180
  , "width": 128
  , "height": 128
}

_UNK_ID = 1
_PAD_ID = 0
MAX_LEN = 5000

datastore_client = datastore.Client.from_service_account_json(DATA_STORE_KEY_PATH, project=PROJECT_ID)


def main():
  writer = tf.python_io.TFRecordWriter(record_file)
  lst, cursor = next_data()
  while lst:
    for obj in lst:
      image = download_image(obj["image_url"])
      image = crop_image(image)
      output = io.BytesIO()
      image.save(output, format='PNG')
      output = output.getvalue()
      width, height = image.size
      ids = text2ids(obj['text'], char_dict)
      record = tf.train.Example(features=tf.train.Features(feature={
        'image': tf.train.Feature(bytes_list=tf.train.BytesList(value=[output])),
        'height': tf.train.Feature(int64_list=tf.train.Int64List(value=[height])),
        'width': tf.train.Feature(int64_list=tf.train.Int64List(value=[width])),
        'depth': tf.train.Feature(int64_list=tf.train.Int64List(value=[3])),
        'text': tf.train.Feature(int64_list=tf.train.Int64List(value=ids))
      }))
      writer.write(record.SerializeToString())
    lst, cursor = next_data(cursor)


def next_data(cursor=None):
  query = datastore_client.query(kind='blog_data')
  query_iter = query.fetch(start_cursor=cursor, limit=300)
  page = next(query_iter.pages)
  next_cursor = query_iter.next_page_token
  data = list(page)
  return data, next_cursor


def text2ids(text, char_dict):
  ids =  list(map(lambda c: char_dict[c] if c in char_dict else _UNK_ID, text[:MAX_LEN]))
  ids = ids + [_PAD_ID for _ in range(MAX_LEN - len(ids))]
  return ids


def load_char_dict():
  with open('./config/all_chars.csv') as f:
    # _PADと＿UNKの分
    return {c.strip():i+2 for i, c in enumerate(f)}


def download_image(url):
  response = urllib.request.urlopen(url)
  return Image.open(io.BytesIO(response.read()))
  

def crop_image(img):
  img.thumbnail((params["thumnail_width"], params["thumnail_height"]), Image.ANTIALIAS)
  #横幅、縦幅を抜き出す
  width, height = img.size
  #画像サイズを加工
  square_size = min(img.size)

  if width > height:
      top = 0
      bottom = square_size
      left = (width - square_size) / 2
      right = left + square_size
      box = (left, top, right, bottom)
  else:
      left = 0
      right = square_size
      top = (height - square_size) / 2
      bottom = top + square_size
      box = (left, top, right, bottom)
  img = img.crop(box)
  return img.resize((params["width"], params["height"]))


if __name__ == '__main__':
  main()