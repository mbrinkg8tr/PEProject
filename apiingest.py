import json
import boto3


def get_db_connection():
    return boto3.resource('dynamodb', region_name='us-east-1')


def get_event_table(db=None):
    if not db:
        db = get_db_connection()

    event_table_name = 'Events'
    region_table_names = [table.name for table in db.tables.all()]
    if event_table_name not in region_table_names:
        return db.create_table(
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
    print(events.name)
    events.put_item(Item=out_event)


f = open('F01705150050.json',)

rpost = json.load(f)
write_event(in_event=rpost)

f.close()


f = open('F01705150090.json',)

rpost = json.load(f)
write_event(in_event=rpost)

f.close()
