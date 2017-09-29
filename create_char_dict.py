# -*- coding: utf-8 -*-
import csv
from google.cloud import datastore
from collections import defaultdict

PROJECT_ID = "persian-172808"
DATA_STORE_KEY_PATH = "/home/vagrant/.json_keys/persian-3a9988725cae.json"



def main():
  datastore_client = datastore.Client.from_service_account_json(DATA_STORE_KEY_PATH, project=PROJECT_ID)
  query = datastore_client.query(kind='blog_data')
  offset = 0
  lst = list(query.fetch())
  chars = defaultdict(int)
  lengths = []
  for obj in lst:
    for c in obj['text']:
      chars[c] += 1
    lengths.append(len(obj['text']))
  
  with open('./data/text_len.txt', 'w') as f:
    for l in lengths:
      f.write(str(l) + '\n')

  with open('./data/char_dict.txt', 'w') as f:
    writer = csv.writer(f, lineterminator='\n')
    for i in chars.items():
      writer.writerow(i)
      

if __name__ == '__main__':
  main()