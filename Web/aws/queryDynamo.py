import boto3
import configS3
from boto3.dynamodb.conditions import Key
from botocore.client import Config



def query_username(username, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=configS3.S3_KEY,
            aws_secret_access_key=configS3.S3_SECRET,
            aws_session_token=configS3.SESSION_TOKEN,
            region_name = configS3.LOCATION,
            config=Config(signature_version='s3v4')
        )

    table = dynamodb.Table('Utenti')
    response = table.query(
        KeyConditionExpression=Key('NomeUtente').eq(username)
    )
    return response['Items']


#if __name__ == '__main__':
    #username = "alessio"
    #print(f"Nome utente: {username}")
    #utenti = query_username(username)
    #for movie in utenti:
    #    print(movie['NomeUtente'])