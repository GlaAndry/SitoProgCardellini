import boto3
import configS3
from botocore.client import Config



def create_utenti_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=configS3.S3_KEY,
            aws_secret_access_key=configS3.S3_SECRET,
            aws_session_token=configS3.SESSION_TOKEN,
            region_name = configS3.LOCATION,
            config=Config(signature_version='s3v4')
        )

    table = dynamodb.create_table(
        TableName='Utenti',
        KeySchema=[
            {
                'AttributeName': 'NomeUtente',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'Password',
                'KeyType': 'RANGE'  # Sort key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'NomeUtente',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Password',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


def create_utenti_resize_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=configS3.S3_KEY,
            aws_secret_access_key=configS3.S3_SECRET,
            aws_session_token=configS3.SESSION_TOKEN,
            region_name = configS3.LOCATION,
            config=Config(signature_version='s3v4')
        )

    table = dynamodb.create_table(
        TableName='resizeTable',
        KeySchema=[
            {
                'AttributeName': 'NomeUtente',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'Resize',
                'KeyType': 'RANGE'  # Sort key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'NomeUtente',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'Resize',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table

if __name__ == '__main__':

    print("Creazione delle tabelle...\n")
    #utenti_table = create_utenti_table()
    #utenti_resize_table=create_utenti_resize_table()
    print("Fatto!\n")
    #print("Table status:", utenti_table.table_status)
