import boto3
from botocore.client import Config
import configS3
import os, tempfile
from PIL import Image, ImageEnhance


##Il session token risulta essere necessario quando si utilizza un account AWSEducate. In particolare deve essere aggiunto a boto3. Se non 
##Dovesse essere presente allora la funzione restituirebbe un errore.
##Le informazioni come KEY_ID, Secret_key e session_token sono disponibili nella workbench, cliccando sul pulsante account details.

ACCESS_KEY_ID = configS3.S3_KEY
ACCESS_SECRET_KEY = configS3.S3_SECRET
SESSION_TOKEN = configS3.SESSION_TOKEN
S3_BUCKET_NOTUSER = configS3.S3_BUCKET_BeW
S3_BUCKET_BEW = configS3.S3_BUCKET_BeW_AFTER

basePath = '/home/alessio/Scrivania/Cardellini/SitoProgCardellini/Web/Functions/'

data = open(basePath+'images/img.png', 'rb')

s3 = boto3.resource(
    's3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY,
    aws_session_token=SESSION_TOKEN,
    config=Config(signature_version='s3v4')
)
#s3.Bucket(BUCKET_NAME).put_object(Key='prova4.png', Body=data)

def blackAndWhite(imgName, userName):
    ##Function for BeW an image:
        #imgName: str --> identifica il nome della risorsa. Deve necessariamente 
        #contenere anche l'estensione. eg: prova.png

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            print("scarico da s3")
            print(imgName)
            os.mkdir(tmpdir+"/"+userName)
            s3.Bucket(S3_BUCKET_NOTUSER).download_file(imgName, tmpdir+"/"+userName+"/"+imgName)
            print("fatto")
            img = Image.open(tmpdir+"/"+userName+"/"+imgName)
            img = img.convert('L')
            img.save(tmpdir+"/"+userName+"/"+imgName) 
            data = open(tmpdir+"/"+userName+"/"+imgName, 'rb')
            print("inserisco in s3")
            s3.Bucket(S3_BUCKET_BEW).put_object(Key=userName+"/"+imgName, Body=data)
            print("fatto")

    except IOError as e:
        print("Impossibile trovare l'immagine")
        print(e)


def changeBrightness_reg(imgName, factor, userName):
    ##Function for resizing an image:
        #wSize: int --> Largezza
        #hSize: int --> Altezza
        #imgName: str --> identifica il nome della risorsa. Deve necessariamente 
        #contenere anche l'estensione. eg: prova.png

    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            print("scarico da s3")
            os.mkdir(tmpdir+"/"+userName)
            s3.Bucket('s3brightnessbucket').download_file(userName+"/"+imgName, tmpdir+"/"+userName+"/"+imgName)
            print("fatto")
            img = Image.open(tmpdir+"/"+userName+"/"+imgName)
            enancher = ImageEnhance.Brightness(img)
            img = enancher.enhance(factor)
            img.save(tmpdir+"/"+userName+"/"+imgName) 
            data = open(tmpdir+"/"+userName+"/"+imgName, 'rb')
            print("inserisco in s3")
            s3.Bucket('s3brightnessbucket-after').put_object(Key=userName+"/"+imgName, Body=data)
            print("fatto")

    except IOError as e:
        print("Impossibile trovare l'immagine")
        print(e)

#changeBrightness_reg("sansone.png", 1, "alessio.mazzola.95@gmail.com")
#blackAndWhite("pro.png","alessio.mazzola.95@gmail.com")

print ("Done")