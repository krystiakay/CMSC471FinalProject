import json
import os
import boto3

textract = boto3.client('textract')
dynamodb = boto3.resources('dynamodb')


def handler(event, context):
    job_id = event['jobId']
    filename = event['filename']
    bucket = event['bucket']
    response = textract.detect_document_text(
        Document={
            'S3Object': {
                'Bucket': bucket, 
                'Name': filename
            }
        }
    )
    items = [
        block['Text'] 
        for block in response['Blocks']
        if block['BlockType'] == 'LINE'
    ]

    dynamodb.Table(os.environ['JOB_TABLE']).update_item(
            Key={'jobId': job_id},
            UpdateExpression='SET #s = :s, #m = :m',
            ExpressionAttributeNames={
                '#s': 'status',
                '#m': 'message'
            },
            ExpressionAttributeValues={
                ':s': 'PROCESSING',
                ':m': f'Textract found {len(items)} items'
            }

        )

    

    # Log the event argument for debugging and for use in local development.
    print(json.dumps(event))

    return {
        'jobId': job_id,
        'items': items 
    }