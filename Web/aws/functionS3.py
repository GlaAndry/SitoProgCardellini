import boto3
from botocore.client import Config

##Il session token risulta essere necessario quando si utilizza un account AWSEducate. In particolare deve essere aggiunto a boto3. Se non 
##Dovesse essere presente allora la funzione restituirebbe un errore.
##Le informazioni come KEY_ID, Secret_key e session_token sono disponibili nella workbench, cliccando sul pulsante account details.

def addToBucket(imgPath, imgName, s3, BUCKET_NAME):
    #La funzione aggiunge l'immagine all'interno del bucket desiderato.
    #imgPath: str --> path locale del file
    #imgName: str --> nome del file una volta inserito all'interno del bucket.
    try:
        data = open(imgPath, 'rb')
    except IOError:
        print("Errore nel caricamento dell'immagine.")
        exit(1)

    
    s3.Bucket(BUCKET_NAME).put_object(Key=imgName, Body=data)
    print('Upload eseguito correttamente.')

def removeFromBucket(removeKey, s3, BUCKET_NAME):
    #La funzione va a rimuovere il file desiderato all'interno del bucket.
    #removeKey: str --> rappresenta il nome del file all'interno del bucket.
    ##Ricordare di aggiungere anche l'estensione, se presente.
    s3.Object(BUCKET_NAME, removeKey).delete()
    print('Rimozione eseguita correttamente.')

def downloadFromBucket(imgPath, imgName, BUCKET_NAME, s3):
    ##La funzione esegue il download di una determinata immagine all'interno del bucket
    #imgPath: str --> path locale del file
    #imgName: str --> nome del file una volta inserito all'interno del bucket.
    
    s3.Bucket(BUCKET_NAME).download_file(imgName, imgPath)
    print("Download eseguito correttamente.")
    