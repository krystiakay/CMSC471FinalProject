import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['RECORDS_TABLE'])

def handler(event, context):
    # event['httpMethod'] says its a GET or DELETE 
    method = event['httpMethod']

    if method == 'GET':
        return get_records()
    
    if method == 'DELETE':
        # /api/records/{id} in path parameters
        record_id = event['pathParameters']['id']
        return delete_record(record_id)
    
    # Log the event argument for debugging and for use in local development.
    print(json.dumps(event))

    return { 'statusCode': 405, 'body': 'Method Not Allowed' }

def get_records():
    result = table.scan() #loading records
    rows = [ ]

    for r in result.get('Items', []):
        rows.append({
            'id': r['id'],
            'item': r['item'],
            'created_at': r.get('created_at', '')
        }) 
    rows.sort(key=lambda x: x['created_at'])
    print(json.dumps(rows))

    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
        'body': json.dumps(rows)
    }

def delete_record(record_id):
    table.delete_item(Key={'id': record_id})
    return {
        'statusCode': 200,
        'headers': {'Access-Control-Allow-Origin': '*'},
    }
