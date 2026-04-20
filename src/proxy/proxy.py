import boto3
import os
import json

s3 = boto3.client('s3')
def proxy_handler(event, context):
    # Log the event argument for debugging and for use in local development.
    print(json.dumps(event))

    # gets the name of the bucket from env vars
    bucket = os.environ.get('BUCKET_BUCKET_NAME')

    #fetch the file
    response = s3.get_object(Bucket=bucket, Key='index.html')
    html_body = response['Body'].read().decode('utf-8')
    
    return {
        'statusCode': 200,
        'body': html_body,
        'headers': {
            'Content-Type': 'text/html'
        }
    }