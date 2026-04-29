import json
import boto3
import os
from botocore.config import Config

s3 = boto3.client(
    's3',
    region_name ='us-east-1',
    config=Config(signature_version='s3v4') # Force V4 signing
    )
BUCKET = os.environ['INBOX_BUCKET_NAME']

def handler(event, context):
    method = event['httpMethod']
    headers = {'Access-Control-Allow-Origin': '*'}

    def error(status_code, message):
        return {
            'statusCode': status_code,
            'headers': headers,
            'body': json.dumps({'message': message})
        }

    if method == 'GET':
        response = s3.list_objects_v2(Bucket=BUCKET)
        files = [obj['Key'] for obj in response.get('Contents', [])]
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps(files)
        }
    
    if method == 'POST':
        try:
            body = json.loads(event.get('body') or '{}')
        except json.JSONDecodeError:
            return error(400, 'Request body must be valid JSON')

        filename = body.get('filename')
        content_type = body.get('contentType') or 'image/png'

        if not filename:
            return error(400, 'filename is required')

        url = s3.generate_presigned_url(
            'put_object', 
            Params={'Bucket': BUCKET, 
                    'Key': filename,
                    'ContentType': content_type}, 
            ExpiresIn=300)
        
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'url': url, 'key': filename})
        }
    
    if method == 'DELETE':
        path_parameters = event.get('pathParameters') or {}
        key = path_parameters.get('key')

        if not key:
            return error(400, 'key is required')

        s3.delete_object(Bucket=BUCKET, Key=key)
        return{
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'message': f'{key} deleted'})
        }

    # Log the event argument for debugging and for use in local development.
    print(json.dumps(event))

    return {}