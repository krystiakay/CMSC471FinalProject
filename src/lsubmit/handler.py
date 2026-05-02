import json
import os
import boto3
import uuid
from datetime import datetime, timezone

dynamodb = boto3.resource('dynamodb')
sfn = boto3.client('stepfunctions')

def handler(event, context):
    body = json.loads(event['body'])
    filename = body['filename']
    job_id = str(uuid.uuid4())

    dynamodb.Table(os.environ['JOB_TABLE']).put_item( 
        Item={
            'job_id': job_id,
            'status': 'RUNNING',
            'message': 'Job is received, starting...',
            'created_at': datetime.now(timezone.utc).isoformat(),
    })

    sfn.start_execution(
        stateMachineArn=os.environ['STATE_MACHINE_ARN'],
        name=job_id,
        input=json.dumps({
            'jobId': job_id,
            'filename': filename
        })

    )

    # Log the event argument for debugging and for use in local development.
    print(json.dumps(event))

    return {
        'statusCode': 200,
        'headers': {'access-control-allow-origin': '*'},
        'body': json.dumps({'jobId': job_id})
    }