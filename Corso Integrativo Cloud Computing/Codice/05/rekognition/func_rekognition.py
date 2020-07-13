# Triggered by any object creation in a given bucket, w prefix "images/"

import boto3
import json

def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    rekognition_client = boto3.client('rekognition')
    for record in event['Records']:                                             
        bucket = record['s3']['bucket']['name']                                 
        key = record['s3']['object']['key']
        
        image_s3 = {
            'S3Object': {
            'Bucket': bucket, 'Name': key
            }
        }
        response = rekognition_client.detect_labels(
             Image=image_s3,
                 MaxLabels=10
        )
        labels = response["Labels"]
        
        newkey = "rek_" + key + ".txt"
        object = s3.Object(bucket, newkey)
        object.put(Body=json.dumps(labels).encode('utf-8'))

    return {
        'statusCode': 200,
        'body': json.dumps(labels)
    }

