import boto3
from botocore.client import Config
import configS3

##Il session token risulta essere necessario quando si utilizza un account AWSEducate. In particolare deve essere aggiunto a boto3. Se non 
##Dovesse essere presente allora la funzione restituirebbe un errore.
##Le informazioni come KEY_ID, Secret_key e session_token sono disponibili nella workbench, cliccando sul pulsante account details.

ACCESS_KEY_ID = configS3.S3_KEY
ACCESS_SECRET_KEY = configS3.S3_SECRET
SESSION_TOKEN = configS3.SESSION_TOKEN
BUCKET_NAME = configS3.S3_BUCKET

basePath = '/home/alessio/Scrivania/Cardellini/SitoProgCardellini/Web/Functions/'

data = open(basePath+'images/img.png', 'rb')

s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    aws_session_token=SESSION_TOKEN,
    config=Config(signature_version='s3v4')
)
s3.Bucket(BUCKET_NAME).put_object(Key='prova4.png', Body=data)

print ("Done")