import boto3

BUCKET='sdcchandson2'
DYNAMO_TABLE='sdccgallery'
QUEUE_NAME='handson-queue'
REGION='eu-central-1'

def get_s3_bucket():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET)
    return bucket

def get_dynamo_table():
    dynamodb = boto3.resource('dynamodb',  region_name=REGION)
    table = dynamodb.Table(DYNAMO_TABLE)
    return table

def get_sqs_queue():
    sqs = boto3.resource('sqs', region_name=REGION)
    try:
        queue = sqs.create_queue(QueueName=QUEUE_NAME)
    except:
        queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)
    return queue

def get_s3_fullpath(key):
    return "https://{}.s3.amazonaws.com/{}".format(BUCKET, key)
