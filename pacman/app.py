import os
import boto3
from botocore.exceptions import ClientError
from chalice import Chalice

app = Chalice(app_name='pacman')
app.debug = True

# Set the value of APP_BUCKET_NAME in the .chalice/config.json file.
S3_BUCKET = os.environ.get('BUCKET_NAME', 'dsac-uva-cloud-2')

@app.on_s3_event(bucket=S3_BUCKET, events=['s3:ObjectCreated:*'])
def s3_handler(event):
    app.log.debug("Received event for bucket: %s, key: %s", event.bucket, event.key)
    try:
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=event.bucket, Key=event.key)
        app.log.debug("Response: %s", response)
        count = len(open(response['Body']).readlines())
        app.log.debug("Line Count: %s", count)
    except ClientError as e:
        app.log.error("Error: %s", e)
        raise e