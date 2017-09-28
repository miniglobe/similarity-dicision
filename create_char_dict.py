# -*- coding: utf-8 -*-

from google.cloud import datastore


PROJECT_ID = "persian-172808"
DATA_STORE_KEY_PATH = "/home/vagrant/.json_keys/persian-3a9988725cae.json"



def main():
  datastore_client = datastore.Client.from_service_account_json(DATA_STORE_KEY_PATH, project=PROJECT_ID)
  query = datastore_client.query(kind='blog_data')
  offset = 0
  lst = list(query.fetch())
  s = set()
  lengths = []
  for obj in lst:
    s |= set(list(obj['text']))
    lengths.append(len(obj['text']))
  
  with open('./data/text_len.txt', 'w') as f:
    for l in lengths:
      f.write(str(l) + '\n')

  with open('./data/char_dict.txt', 'w') as f:
    for c in s:
      f.write(c + '\n')

if __name__ == '__main__':
  main()