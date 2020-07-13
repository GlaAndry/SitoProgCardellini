from flask import Flask, request, url_for, redirect, render_template 
from Functions import imageFunctions
import os
from aws import functionS3
from aws import configS3
import boto3
from botocore.client import Config
import time
import requests


app = Flask(__name__)

basePath = '/home/alessio/Scrivania/Cardellini/SitoProgCardellini/Web/Functions'
bewPath = '/B&W'
resizePath = '/resized'
saturationPath = '/saturation'
brightnessPath = '/brightness'
imgPath = '/images'


##app config
app.config["IMAGE_UPLOADS"] = "/home/alessio/Scrivania/Cardellini/SitoProgCardellini/Web/Functions/uploadedImages"
app.config["ALLOWED_EXT"] = ["JPG", "PNG", "GIF", "JPEG"]
############


##S3 config############################

### information from configS3
ACCESS_KEY_ID = configS3.S3_KEY
ACCESS_SECRET_KEY = configS3.S3_SECRET
SESSION_TOKEN = configS3.SESSION_TOKEN


BUCKET_NAME_RESIZE = configS3.S3_BUCKET_RESIZE
BUCKET_NAME_BeW = configS3.S3_BUCKET_BeW
BUCKET_NAME_BRIGHTNESS = configS3.S3_BUCKET_BRIGHTNESS
BUCKET_NAME_SATURATION = configS3.S3_BUCKET_SATURATION


s3 = boto3.resource(
        's3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
        config=Config(signature_version='s3v4')
    )
###################################


def allowed_ext(extFile):
    ##La funzione verifica se il file inserito è effettivamente un file consentito o meno.
    if not "." in extFile:
        return False
    ext = extFile.rsplit(".",1)[1]
    if ext.upper() in app.config["ALLOWED_EXT"]:
        return True
    else:
        return False



@app.route('/', methods=['GET','POST'])
def homepage():
    return render_template("index.html")
 
@app.route('/signin')
def signin():
    return render_template("signin.html")

@app.route('/accedi')
def accedi():
    return render_template("accedi.html")

@app.route('/resizeImage')
def resizeImage():
    return render_template("resizeImage.html")

@app.route('/links', methods=['GET','POST'])
def links():
    return render_template("link.html")

@app.route('/black_and_white', methods=['GET','POST'])
def black_and_white():
    return render_template("blackAndWhite.html")






@app.route('/doResize', methods=['GET','POST'])
def do_resize():
    ##resize image
    if request.method == "POST":
        if request.files:
            ##verifico che l'upload dell'imagine è stato effettivamente eseguito
            img = request.files["image"] ##nome del file
            hSize = request.form["hSize"] ##valore altezza
            wSize = request.form["wSize"] ##valore larghezza

            if img.filename == "":
                return redirect(request.url)
            if not allowed_ext(img.filename):
                print("Estensione non supportata dal sistema")
                return redirect(request.url)

            
            img.save(os.path.join(app.config["IMAGE_UPLOADS"], img.filename))
            print(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename)
            ##Eseguo l'upload su s3 in quanto successivamente sfrutto le funzioni lamda.
            functionS3.addToBucket(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename, img.filename, s3, BUCKET_NAME_RESIZE)
            time.sleep(1) ##sleep per permettere il caricamento dell'immagine.
            
            ##rest api lambda
            url = 'https://62j41asgt0.execute-api.us-east-1.amazonaws.com/default/resImg?wSize='+wSize+'&hSize='+hSize+'&imgName='+img.filename
            requests.get(url) ##esecuzione della rest-api
            #####

            ##downloadFunction successiva per ritornare l'immagine una volta che è stata processata dalle lamda.
            ##functionS3.downloadFromBucket("/home/alessio/Scrivania/Cardellini/SitoProgCardellini/Web/Functions/downloadedImages/prova.png", "prova.png", BUCKET_NAME, s3)
            return redirect(request.url)
            
    return render_template("resizeImage.html")

 


if __name__ == "__main__":
	app.run(debug = True, host='127.0.0.1', port=8080, passthrough_errors=True)