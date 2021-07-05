import json
import boto3
import botocore


class ClientException(Exception):
    pass


def get_db_connection():
    return boto3.resource('dynamodb')


def get_event_table(db=None):
    if not db:
        db = get_db_connection()

    event_table_name = 'Events'
    region_table_names = [table.name for table in db.tables.all()]
    if event_table_name not in region_table_names:
        db.create_table(
            TableName='Events',
            KeySchema=[
                {
                    'AttributeName': 'event_id',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'dtg',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'event_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'dtg',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        return db.Table('Events')
    else:
        return db.Table('Events')


def write_event(db=None, in_event=None):
    if not db:
        db = get_db_connection()

    out_event = {
        'event_id': in_event['description']['event_id'],
        'dtg': in_event['description']['event_opened'],
        'info': json.dumps(in_event)
    }
    events = get_event_table(db=db)
    try:
        events.put_item(Item=out_event)
        return out_event
    except botocore.exceptions.ClientError as e:
        raise ClientException(str(e))


def lambda_handler(event, context):
    body = event['body']
    dd = json.loads(body)
    try:
        result = write_event(in_event=dd)
    except Exception as e:
        exception_type = e.__class__.__name__
        exception_message = str(e)

        api_exception_obj = {
            "isError": True,
            "type": exception_type,
            "message": exception_message
        }
        api_exception_json = json.dumps(api_exception_obj)
        raise LambdaException(api_exception_json)

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }

