import json
import boto3
import botocore


class ClientException(Exception):
    pass


def get_db_connection():
    """
    Gets a DynamoDB connection for the lambda context
    :return: a dynamodb database connection object
    """
    return boto3.resource('dynamodb')


def get_event_table(db=None):
    """
    Returns the Events table from the database connection if specified.  If it doesn't exist, it is created.  IRL, the
    creation task is better suited for CodeDeploy or CloudFormation rather than in this lambda function as the table
    might not be ready for consumption immediately after creation.
    :param db: database connection object, or if None, will get one
    :return: the Events table object
    """
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


def write_event(db=None, in_event=None):
    """
    Commits an event to the Events table
    :param db: Database connection, or gets one if None
    :param in_event: The event JSON.  JSON must include event_id and event_opened in the description.  (We would do
    better validation here IRL)
    :return: a JSON object of the committed event if successful.
    :exception Raises a client exception if not successful
    """
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
    """
    Called by the lambda function context when the API is called
    :param event: Event from the API gateway
    :param context: Lambda function context
    :return: echos back the received data for client side validation as an HTTP 200 response
    """
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

