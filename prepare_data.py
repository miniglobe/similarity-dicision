# -*- coding: utf-8 -*-

import tensorflow
from google.cloud import datastore

PROJECT_ID = "persian-172808"
DATA_STORE_KEY_PATH = "/home/vagrant/.json_keys/persian-3a9988725cae.json"
STORAGE_STORE_KEY_PATH = "/home/vagrant/.json_keys/persian-efe392f65854.json"
BUCKET_NAME = "persian-172808.appspot.com"


def main():
  datastore_client = datastore.Client.from_service_account_json(DATA_STORE_KEY_PATH, project=PROJECT_ID)
  query = datastore_client.query(kind='blog_data')
  offset = 0
  lst = list(query.fetch(limit=100, offset=offset))
  while lst:
    print(len(lst))
    offset += 100
    lst = list(query.fetch(limit=100, offset=offset))


if __name__ == '__main__':
  main()