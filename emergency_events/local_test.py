import boto3
from os import listdir
from os.path import isfile, join
from lambda_function import *


# When not running in a lambda context, the region must be specified
def get_db_connection():
    """
    Gets a DynamoDB connection for the lambda context.  Region is specified here for testing purposes
    :return: a dynamodb database connection object
    """
    return boto3.resource('dynamodb', region_name='us-east-1')


if __name__ == "__main__":
    db = get_db_connection()
    working_directory = "../test_data"
    process_files = [d for d in listdir(working_directory) if isfile(join(working_directory, d))]

    """ Iterate through the contents of the working directory and push to the API """
    for data_source_file in process_files:
        f = open(join(working_directory, data_source_file))
        rpost = json.load(f)
        write_event(db=db, in_event=rpost)
        f.close()

