import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('sdccgallery')

# Storing an item
table.put_item(
   Item={
        'imageid': 'provaid',
        'title': 'ruan',
        'tags': ['tag1', 'tag2']
    }
)

# Reading from DynamoDB
key = "provaid"
response = table.get_item(
   Key={
        'imageid': key,
    }
)

item = response['Item']
print(item)
