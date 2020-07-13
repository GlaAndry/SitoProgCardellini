from PIL import Image, ImageEnhance
import boto3
from botocore.client import Config
from __future__ import print_function
import json

s3 = boto3.resource('s3')
S3_BUCKET_NOTUSER = 's3bucketresizefunction'
S3_BUCKET_RESIZED = 's3bucketresizefunction-resized'

print('Loading function')


def lambda_handler(event, context):
    
    wSize = int(event['wSize'])
    hSize = int(event['hSize'])
    inPath = str(event['inPath'])
    outPath = str(event['outPath'])

    resize(wSize,hSize,inPath,outPath)

    return {
        'statuscCode':200,
    }

def resize(wSize, hSize, inPath, outPath):
    ##Function for resizing an image:
        #wSize: int --> Largezza
        #hSize: int --> Altezza
        #inPath: str --> Input Path
        #outPath: str --> Output Path

    try:
        s3.Bucket(S3_BUCKET_NOTUSER).download_file('prova.png', inPath)
        img = Image.open(inPath)
        img = img.resize((wSize, hSize), Image.ANTIALIAS)
        img.save(outPath) 
        data = open(outPath, 'rb')
        s3.Bucket(S3_BUCKET_RESIZED).put_object(Key='prova.png', Body=data)


    except IOError:
        print("Impossibile trovare l'immagine")
        exit(1)

#resize(100,100, '/home/alessio/Scrivania/Cardellini/SitoProgCardellini/Web/Functions/images/prova.jpg', '/home/alessio/Scrivania/Cardellini/SitoProgCardellini/Web/Functions/images/prova2.jpg')