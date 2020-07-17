import boto3
#import configS3
from botocore.client import Config
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key



def create_utenti_table(dynamodb, tableName):
    ##Questa funzione crea una tabella all'interno di DynamoDB
    ##Table --> {NomeUtente, Link S3}

    table = dynamodb.create_table(
        TableName=tableName,
        KeySchema=[
            {
                'AttributeName': 'NomeUtente',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'link',
                'KeyType': 'RANGE'  # Sort key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'NomeUtente',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'link',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table

def add_element_in_table(dynamodb, tableName, nomeUtente, linkS3):
    #Questa funzione inserisce all'interno di DynamoDB gli elementi desiderati.
    table = dynamodb.Table(tableName)
    response = table.put_item(
       Item={
            'NomeUtente': nomeUtente,
            'link': linkS3,
        }
    )
    return response

def get_element_from_table(dynamodb, tableName, nomeUtente):
    #Questa funzione ritorna gli elementi desiderati all'interno della tabella.
    table = dynamodb.Table(tableName)

    try:
        
        #response = table.get_item(Key={'NomeUtente': nomeUtente})
        response = table.query(
            KeyConditionExpression=Key('NomeUtente').eq(nomeUtente)
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response['Items']  



if __name__ == '__main__':

    print("Creazione delle tabelle...\n")
    ##Creiamo la tabella solo la prima volta.
    #create_utenti_table(dynamodb, "Utenti")
    print("Fatto!\n")
    
