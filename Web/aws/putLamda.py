import boto3
from botocore.client import Config
import functionS3
import configS3
import boto3
from botocore.client import Config


##Il session token risulta essere necessario quando si utilizza un account AWSEducate. In particolare deve essere aggiunto a boto3. Se non 
##Dovesse essere presente allora la funzione restituirebbe un errore.
##Le informazioni come KEY_ID, Secret_key e session_token sono disponibili nella workbench, cliccando sul pulsante account details.


##S3 config############################

### information from configS3
ACCESS_KEY_ID = configS3.S3_KEY
ACCESS_SECRET_KEY = configS3.S3_SECRET
SESSION_TOKEN = configS3.SESSION_TOKEN
BUCKET_NAME = configS3.S3_LAMBDASTORE

s3 = boto3.resource(
        's3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
        config=Config(signature_version='s3v4')
    )
###################################

def addToBucket(path, name, s3, BUCKET_NAME):
    #La funzione aggiunge l'immagine all'interno del bucket desiderato.
    #imgPath: str --> path locale del file
    #imgName: str --> nome del file una volta inserito all'interno del bucket.
    try:
        data = open(path, 'rb')
    except IOError:
        print("Errore nel caricamento dell'immagine.")
        exit(1)
    
    s3.Bucket(BUCKET_NAME).put_object(Key=name, Body=data)
    print('Upload eseguito correttamente.')

#addToBucket('/home/alessio/Scrivania/Cardellini/SitoProgCardellini/Web/aws/lambdazip/lambda-resize.zip', 'lambda-resize.zip', s3, BUCKET_NAME)
#addToBucket('/home/alessio/Scrivania/Cardellini/SitoProgCardellini/Web/aws/lambdazip/lambda-bew.zip', 'lambda-bew.zip', s3, BUCKET_NAME)
#addToBucket('/home/alessio/Scrivania/Cardellini/SitoProgCardellini/Web/aws/lambdazip/lambda-bright.zip', 'lambda-bright.zip', s3, BUCKET_NAME)
addToBucket('/home/alessio/Scrivania/Cardellini/SitoProgCardellini/Web/aws/lambdazip/lambda-sat.zip', 'lambda-sat.zip', s3, BUCKET_NAME)