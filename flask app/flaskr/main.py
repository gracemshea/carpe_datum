
from flask import Flask, request, Response, render_template, send_file, url_for
from google.cloud import storage
from google.cloud import pubsub_v1
import pdb
import argparse
import json
import time

app = Flask('__name__')
@app.route('/')
def index():
    return render_template('/static/index.html')

@app.route('/download_files')
def download_files():
    return render_template('result.html')

@app.route('/return-files/')
def return_files():
    try:
        return send_file('', attachment_filename='results.csv')
    except Exception as e:
        return str(e)

@app.route("/upload_csv", methods=["POST"])
def upload_csv():
  file = request.files.get("file")
  if file == None:
    return Response(status=400)
  else:
    success = upload("spaceapps2019", file, file.filename)
    if success:
      #go to loading page
      return render_template('loading.html')
    else:
      return Response(status=400)

@app.route("/loading")

def loading():
    poll_notifications("seal-team-404", "resultsSub")
    send_file('media_link', attachment_filename='.jpg')

def upload(bucket_name, source_file, destination_blob_name):
  """Uploads a file to the bucket."""
  storage_client = storage.Client()
  bucket = storage_client.get_bucket(bucket_name)
  blob = bucket.blob(destination_blob_name)

  try:
    blob.upload_from_file(source_file)
  except:
    return None
  else:
    return('File {} uploaded to {}.'.format(
      source_file,
      destination_blob_name))

def summarize(message):
    # [START parse_message]
    data = message.data.decode('utf-8')
    attributes = message.attributes
    media_link = attributes['mediaLink']
    event_type = attributes['eventType']
    bucket_id = attributes['bucketId']
    object_id = attributes['objectId']
    generation = attributes['objectGeneration']
    description = (
        
        '\tEvent type: {event_type}\n'
        '\tBucket ID: {bucket_id}\n'
        '\tObject ID: {object_id}\n'
        '\tMedia Link: {media_link}\n'
        '\tGeneration: {generation}\n').format(
            event_type=event_type,
            bucket_id=bucket_id,
            object_id=object_id,
            media_link=media_link,
            generation=generation)

    if 'overwroteGeneration' in attributes:
        description += '\tOverwrote generation: %s\n' % (
            attributes['overwroteGeneration'])
    if 'overwrittenByGeneration' in attributes:
        description += '\tOverwritten by generation: %s\n' % (
            attributes['overwrittenByGeneration'])

    payload_format = attributes['payloadFormat']
    if payload_format == 'JSON_API_V1':
        object_metadata = json.loads(data)
        size = object_metadata['size']
        content_type = object_metadata['contentType']
        metageneration = object_metadata['metageneration']
        description += (
            '\tContent type: {content_type}\n'
            '\tSize: {object_size}\n'
            '\tMetageneration: {metageneration}\n').format(
                content_type=content_type,
                object_size=size,
                metageneration=metageneration)
    return description
    # [END parse_message]


def poll_notifications(project, subscription_name):
    messages = []
    """Polls a Cloud Pub/Sub subscription for new GCS events for display."""
    # [BEGIN poll_notifications]
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        project, subscription_name)

    def callback(message):
        print('Received message:\n{}'.format(summarize(message)))
        message.ack()
        media_link=message.attributes.media_link
        return media_link

    subscriber.subscribe(subscription_path, callback=callback)

    # The subscriber is non-blocking, so we must keep the main thread from
    # exiting to allow it to process messages in the background.
    print('Listening for messages on {}'.format(subscription_path))
    while True:
        time.sleep(60)
    # [END poll_notifications]
    return media_link


