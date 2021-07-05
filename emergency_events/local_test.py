import json
import boto3
from lambda_function import *


def get_db_connection():
    return boto3.resource('dynamodb', region_name='us-east-1')


if __name__ == "__main__":
    db = get_db_connection()

    f = open('../test_data/F01705150050.json',)

    rpost = json.load(f)
    write_event(db=db,in_event=rpost)

    f.close()


    f = open('../test_data/F01705150090.json',)

    rpost = json.load(f)
    write_event(db=db,in_event=rpost)

    f.close()
