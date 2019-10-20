import base64
import json
from google.cloud import pubsub_v1
from tweepy import StreamListener

import settings

class UploadListener(StreamListener):
  client = pubsub_v1.PublisherClient()
  topic_path = client.topic_path(seal-team-404, uploadReady)
  count = 0
  files = []
  batch_size = 1
  total_files = 1000

def publish(client, topic_path, data_lines):
    messages = []
    for line in data_lines:
        messages.append({'data': line})
    body = {'messages': messages}
    str_body = json.dumps(body)
    data = base64.urlsafe_b64encode(bytearray(str_body, 'utf8'))
    client.publish(topic_path, data=data)

def write_to_pubsub(self, tw):
        publish(self.client, self.topic_path, tw)

def on_status(self, status):
# Medium article had this logic, doesn't appear to apply
# print(tw)
# self.tweets.append(tw)
# if len(self.tweets) >= self.batch_size:
#     self.write_to_pubsub(self.tweets)
#     self.tweets = []

# self.count += 1
# if self.count >= self.total_tweets:
#     return False
# if (self.count % 50) == 0:
#     print("count is: {}".format(self.count))
# return True

def on_error(self, status_code):
  print(status_code)