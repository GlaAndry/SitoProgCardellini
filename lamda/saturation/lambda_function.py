from __future__ import print_function
from PIL import Image, ImageEnhance
import boto3
from botocore.client import Config
import json
import os, tempfile

s3 = boto3.resource(
        's3',
        aws_access_key_id='ASIAYEAFIJNSPQUFSM5C',
        aws_secret_access_key='xmnNJc3d9yHyoMTG0VBEoGWHCJvuAdoRbqpalJk5',
        aws_session_token='FwoGZXIvYXdzEOH//////////wEaDG8TW4XW7u1tDe7PpSLLARRpO5IydGbec/U3noVVr+V/LuVotVGPsC0XdKLEqhPP4OONdq0emU9tbuGKImk1A8vbSlJLADdntNWdVNrvZQAI/71wG+efmVlO8Hi8M30dcUhy7DSMkD2QQ9FniU7FHqOPzl4xxhSR4VQafvCtG7rXnf2GAPSFo9i5M/l4ZIh5Su1d64kd5jfI7H9AdzpRIBTxvGExHJSrKqj9S11GHXmEJSEure8WnnzCtssfC4YgMHu0ff/mBgxyb016JfnjfyEc7lxZYJeHEoDmKLPzsfgFMi21zw3hDMl1v6BBZV5EPxhJOeEwvh7rXbotvUYhu76/hjPf3R/yynHAOfvQKmA=',
        config=Config(signature_version='s3v4')
    )
S3_BUCKET_NOTUSER = 's3saturationbucket'
S3_BUCKET_BEW = 's3saturationbucket-after'

print('Loading function')


def lambda_handler(event, context):
    
    imgName = str(event['imgName'])
    factor = int(event['factor'])

    print(imgName)
    print(factor)

    print("Eseguo la funzione resize...")
    changeSaturation(imgName, factor)
    print("fatto")

    return {
        'statuscCode':200,
    }


def changeSaturation(imgName, factor):
    ##Function for resizing an image:
        #wSize: int --> Largezza
        #hSize: int --> Altezza
        #imgName: str --> identifica il nome della risorsa. Deve necessariamente 
        #contenere anche l'estensione. eg: prova.png

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            print("scarico da s3")
            s3.Bucket(S3_BUCKET_NOTUSER).download_file(imgName, tmpdir+"/"+imgName)
            print("fatto")
            img = Image.open(tmpdir+"/"+imgName)
            enancher = ImageEnhance.Color(img)
            img = enancher.enhance(factor)
            img.save(tmpdir+"/"+imgName) 
            data = open(tmpdir+"/"+imgName, 'rb')
            print("inserisco in s3")
            s3.Bucket(S3_BUCKET_BEW).put_object(Key=imgName, Body=data)
            print("fatto")

    except IOError as e:
        print("Impossibile trovare l'immagine")
        print(e)