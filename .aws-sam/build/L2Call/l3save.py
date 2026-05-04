import json
import boto3
import os
import uuid
from datetime import datetime, timezone

dynamodb = boto3.resource('dynamodb') #low level interface. must specify data types explicitly
#

#rds = boto3.client('rds-data')

def handler(event, context):
    job_id = event['jobId']
    items = event['items']
   

    records_table = dynamodb.Table(os.environ['JOB_TABLE'])
    for item in items:
        records_table.put_item(Item={
                'id': str(uuid.uuid4()),
                'job_id': job_id,
                'item': item,
                'created_at': datetime.now(timezone.utc).isoformat()
            })
       

    dynamodb.Table(os.environ['JOB_TABLE']).update_item(
            Key={'jobId': job_id},
            UpdateExpression='SET #s = :v1, #m = :v2',
            ExpressionAttributeNames={
                '#s': 'status',
                '#m': 'message'
            },
            ExpressionAttributeValues={
                ':v1': 'SUCCEEDED',
                ':v2': f'Saved {len(items)} items to the table'
            }
    )

    # Log the event argument for debugging and for use in local development.
    print(json.dumps(event))

    return {
        'jobId': job_id,
        'rowCount': len(items)
    }