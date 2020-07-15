from flask import Flask, request, url_for, redirect, render_template, send_file
from Functions import imageFunctions
import os
from aws import functionS3
from aws import configS3
from aws import functionCognito
import boto3
from botocore.client import Config
import time
import requests


# from aws import queryDynamo


app = Flask(__name__)

basePath = '/home/alessio/Scrivania/Cardellini/SitoProgCardellini/Web/Functions'
bewPath = '/B&W'
resizePath = '/resized'
saturationPath = '/saturation'
brightnessPath = '/brightness'
imgPath = '/images'

global nomeUtente 
nomeUtente = ""

global isDownloaded
isDownloaded = 0

global imgNameDownload
imgNameDownload = ""

# app config
# app.config["IMAGE_UPLOADS"] = "/home/alessio/Scrivania/Cardellini/SitoProgCardellini/Web/Functions/uploadedImages" ###UBUNTU
app.config["IMAGE_UPLOADS"] = "/Users/alessio/SitoProgCardellini/Web/resources/imageUpload"  #MAC
app.config["IMAGE_DOWNLOADS"]= "/Users/alessio/SitoProgCardellini/Web/resources/imageDownload" #MAC
app.config["ALLOWED_EXT"] = ["JPG", "PNG", "GIF", "JPEG"]
############


##AWS config############################
ACCESS_KEY_ID = configS3.S3_KEY
ACCESS_SECRET_KEY = configS3.S3_SECRET
SESSION_TOKEN = configS3.SESSION_TOKEN


BUCKET_NAME_RESIZE = configS3.S3_BUCKET_RESIZE
BUCKET_NAME_BeW = configS3.S3_BUCKET_BeW
BUCKET_NAME_BRIGHTNESS = configS3.S3_BUCKET_BRIGHTNESS
BUCKET_NAME_SATURATION = configS3.S3_BUCKET_SATURATION

# S3
s3 = boto3.resource(
        's3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
        config=Config(signature_version='s3v4')
    )

# DYNAMODB
dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=configS3.S3_KEY,
            aws_secret_access_key=configS3.S3_SECRET,
            aws_session_token=configS3.SESSION_TOKEN,
            region_name=configS3.LOCATION,
            config=Config(signature_version='s3v4')
        )

#COGNITO
cognito = boto3.client('cognito-idp',
            aws_access_key_id=configS3.S3_KEY,
            aws_secret_access_key=configS3.S3_SECRET,
            aws_session_token=configS3.SESSION_TOKEN,
            region_name = configS3.LOCATION,
)

cognito_id = boto3.client('cognito-identity',
            aws_access_key_id=configS3.S3_KEY,
            aws_secret_access_key=configS3.S3_SECRET,
            aws_session_token=configS3.SESSION_TOKEN,
            region_name = configS3.LOCATION,
)

###################################


def allowed_ext(extFile):
    # La funzione verifica se il file inserito è effettivamente un file consentito o meno.
    if not "." in extFile:
        return False
    ext = extFile.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_EXT"]:
        return True
    else:
        return False


@app.route('/', methods=['GET', 'POST'])
def homepage():
    return render_template("index.html")


@app.route('/signin')
def signin():
    return render_template("signin.html")

@app.route('/doSignin', methods=['GET', 'POST'])
def do_signin():
    
    ##verifico che ci sia un evento di post
    if request.method == "POST":

        #prendo i valori inseriti dall'utente
        email = request.form["inputEmail"]
        userName = request.form["inputUserName"] 
        password = request.form["inputPassword"]
        ##
        #invio la richiesta di registrazione a cognito.
        try:
            functionCognito.register_user(userName,email,password,configS3.CLIENTID, cognito)
        except Exception as e:
            print(e)
            return render_template("alreadyExistingUser.html")
        

        return render_template("registration.html")



    return render_template("signin.html")


@app.route('/accedi')
def accedi():
    return render_template("accedi.html")

@app.route('/doAccedi', methods=['GET', 'POST'])
def do_accedi():
    
    ##verifico che ci sia un evento di post
    if request.method == "POST":

        #prendo i valori inseriti dall'utente
        email = request.form["inputEmail"]
        password = request.form["inputPassword"]
        ##
        #verifico tramite cognito se le credenziali di accesso siano corrette.
        try:
            functionCognito.accedi_user(configS3.CLIENTID, email, password, cognito)
        
            ##Variabile impostata una volta che viene eseguito l'accesso!
            global nomeUtente
            nomeUtente = email
            #################

            return render_template("accediOK.html")

        except Exception as e:
            print(e)
            return render_template("alreadyExistingUser.html")
        

        return render_template("registration.html")



    return render_template("signin.html")

@app.route('/resizeImage')
def resizeImage():
    return render_template("resizeImage.html")


@app.route('/black_and_white')
def black_and_white():
    return render_template("blackAndWhite.html")


@app.route('/saturation')
def saturation():
    return render_template("saturation.html")


@app.route('/brightness')
def brightness():
    return render_template("brightness.html")


@app.route('/links', methods=['GET', 'POST'])
def links():
    return render_template("link.html")


@app.route('/doBeW', methods=['GET','POST'])
def doBeW():
    # blackAndWhite image

    # verifico che l'utente sia registrato o meno.
    # "INSERIRE LA VARIABILE PER IL NOME UTENTE."
    # username = queryDynamo.query_username("alessio")
    username = nomeUtente

    ##
    global isDownloaded
    isDownloaded = 0

    global imgNameDownload


    if request.method == "POST":
        if request.files:
            # verifico che l'upload dell'imagine è stato effettivamente eseguito
            img = request.files["image"] ##nome del file


            # controllo che venga eseguito l'upload dell'immagine
            if img.filename == "":
                return redirect(request.url)
            if not allowed_ext(img.filename):
                print("Estensione non supportata dal sistema")
                return redirect(request.url)

            img.save(os.path.join(app.config["IMAGE_UPLOADS"], img.filename))


            if username:
                print(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename)
                # Eseguo l'upload su s3 in quanto successivamente sfrutto le funzioni lamda.
                functionS3.addToBucket(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename, username+"/"+img.filename, s3, BUCKET_NAME_BeW)
                #time.sleep(1) ##sleep per permettere il caricamento dell'immagine.
                
                # rest api lambda
                url = 'https://3fsi3za5x1.execute-api.us-east-1.amazonaws.com/default/bewImg?&imgName='+img.filename
                requests.get(url) ##esecuzione della rest-api
                #####

                # downloadFunction successiva per ritornare l'immagine una volta che è stata processata dalle lamda.
                functionS3.downloadFromBucket(os.path.join(app.config["IMAGE_DOWNLOADS"])+"/"+img.filename, username+"/"+img.filename, BUCKET_NAME_BeW, s3)
                
                isDownloaded = 1
                global imgNameDownload
                imgNameDownload = img.filename

                #return render_template("download.html")
                return render_template("download.html")
            else:
                print(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename)
                # Eseguo l'upload su s3 in quanto successivamente sfrutto le funzioni lamda.
                functionS3.addToBucket(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename, img.filename, s3, BUCKET_NAME_BeW)
                time.sleep(1) ##sleep per permettere il caricamento dell'immagine.
                
                # rest api lambda
                url = 'https://3fsi3za5x1.execute-api.us-east-1.amazonaws.com/default/bewImg?&imgName='+img.filename
                #requests.get(url) ##esecuzione della rest-api
                #####

                # downloadFunction successiva per ritornare l'immagine una volta che è stata processata dalle lamda.
                functionS3.downloadFromBucket(os.path.join(app.config["IMAGE_DOWNLOADS"])+"/"+img.filename, img.filename, BUCKET_NAME_BeW, s3)
                isDownloaded = 1
                imgNameDownload = img.filename
                return render_template("download.html")
                #return render_template("download.html")
    else:
        return render_template("blackAndWhite.html")

    return render_template("blackAndWhite.html")


@app.route('/doResize', methods=['GET','POST'])
def do_resize():
    # resize image

    # verifico che l'utente sia registrato o meno.
    # "INSERIRE LA VARIABILE PER IL NOME UTENTE."
    # username = queryDynamo.query_username("alessio")
    username = nomeUtente


    if request.method == "POST":
        if request.files:
            # verifico che l'upload dell'imagine è stato effettivamente eseguito
            img = request.files["image"] ##nome del file
            hSize = request.form["hSize"] ##valore altezza
            wSize = request.form["wSize"] ##valore larghezza

            # controllo che venga eseguito l'upload dell'immagine
            if img.filename == "": 
                return redirect(request.url)
            # verifico che le misure siano corrette    
            if hSize == "0" or wSize == "0":
                return redirect(request.url)
            if not allowed_ext(img.filename):
                print("Estensione non supportata dal sistema")
                return redirect(request.url)

            
            img.save(os.path.join(app.config["IMAGE_UPLOADS"], img.filename))

            

            if username:
                print(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename)
                # Eseguo l'upload su s3 in quanto successivamente sfrutto le funzioni lamda.
                functionS3.addToBucket(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename, username+"/"+img.filename, s3, BUCKET_NAME_RESIZE)
                time.sleep(1) ##sleep per permettere il caricamento dell'immagine.
                
                # rest api lambda
                url = 'https://62j41asgt0.execute-api.us-east-1.amazonaws.com/default/resImg?wSize='+wSize+'&hSize='+hSize+'&imgName='+img.filename
                requests.get(url) ##esecuzione della rest-api
                #####

                # downloadFunction successiva per ritornare l'immagine una volta che è stata processata dalle lamda.
                # functionS3.downloadFromBucket("/home/alessio/Scrivania/Cardellini/SitoProgCardellini/Web/Functions/downloadedImages/prova.png", "prova.png", BUCKET_NAME, s3)
                return redirect(request.url)
            else:
                print(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename)
                # Eseguo l'upload su s3 in quanto successivamente sfrutto le funzioni lamda.
                functionS3.addToBucket(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename, img.filename, s3, BUCKET_NAME_RESIZE)
                time.sleep(1) ##sleep per permettere il caricamento dell'immagine.
                
                # rest api lambda
                url = 'https://62j41asgt0.execute-api.us-east-1.amazonaws.com/default/resImg?wSize='+wSize+'&hSize='+hSize+'&imgName='+img.filename
                requests.get(url) ##esecuzione della rest-api
                #####

                # downloadFunction successiva per ritornare l'immagine una volta che è stata processata dalle lamda.
                # functionS3.downloadFromBucket("/home/alessio/Scrivania/Cardellini/SitoProgCardellini/Web/Functions/downloadedImages/prova.png", "prova.png", BUCKET_NAME, s3)
                return redirect(request.url)
            
    return render_template("resizeImage.html")


@app.route('/doBrightness', methods=['GET','POST'])
def do_brightness():
    # brightness image

    # verifico che l'utente sia registrato o meno.
    # "INSERIRE LA VARIABILE PER IL NOME UTENTE."
    # username = queryDynamo.query_username("alessio")
    username = nomeUtente

    print("Ecco il nome:")
    print(nomeUtente)

    if request.method == "POST":
        if request.files:
            # verifico che l'upload dell'imagine è stato effettivamente eseguito
            img = request.files["image"] ##nome del file
            factor = request.form["factor"] ##valore factor per la brightness
            # controllo che venga eseguito l'upload dell'immagine
            if img.filename == "": 
                return redirect(request.url)
            # verifico che le misure siano corrette    
            if factor == "0":
                print("Inserire un valore di factor diverso da 0")
                return redirect(request.url)
            if not allowed_ext(img.filename):
                print("Estensione non supportata dal sistema")
                return redirect(request.url)

            
            img.save(os.path.join(app.config["IMAGE_UPLOADS"], img.filename))

            if username:
                print(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename)
                # Eseguo l'upload su s3 in quanto successivamente sfrutto le funzioni lamda.
                functionS3.addToBucket(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename, username+"/"+img.filename, s3, BUCKET_NAME_BRIGHTNESS)
                time.sleep(1) ##sleep per permettere il caricamento dell'immagine.
                
                # rest api lambda
                url = 'https://jx902kdqgc.execute-api.us-east-1.amazonaws.com/default/brightnessimg?imgName='+img.filename+'&factor='+factor
                requests.get(url) ##esecuzione della rest-api
                #####

                # downloadFunction successiva per ritornare l'immagine una volta che è stata processata dalle lamda.
                # functionS3.downloadFromBucket("/home/alessio/Scrivania/Cardellini/SitoProgCardellini/Web/Functions/downloadedImages/prova.png", "prova.png", BUCKET_NAME, s3)
                return redirect(request.url)
            else:
                print(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename)
                # Eseguo l'upload su s3 in quanto successivamente sfrutto le funzioni lamda.
                functionS3.addToBucket(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename, img.filename, s3, BUCKET_NAME_BRIGHTNESS)
                time.sleep(1) ##sleep per permettere il caricamento dell'immagine.
                
                # rest api lambda
                url = 'https://jx902kdqgc.execute-api.us-east-1.amazonaws.com/default/brightnessimg?imgName='+img.filename+'&factor='+factor
                requests.get(url) ##esecuzione della rest-api
                #####

                # downloadFunction successiva per ritornare l'immagine una volta che è stata processata dalle lamda.
                # functionS3.downloadFromBucket("/home/alessio/Scrivania/Cardellini/SitoProgCardellini/Web/Functions/downloadedImages/prova.png", "prova.png", BUCKET_NAME, s3)
                return redirect(request.url)
            
    return render_template("brightness.html")


@app.route('/doSaturation', methods=['GET','POST'])
def do_saturation():
    # saturation image

    # verifico che l'utente sia registrato o meno.
    # "INSERIRE LA VARIABILE PER IL NOME UTENTE."
    # username = queryDynamo.query_username("alessio")
    username = nomeUtente

    if request.method == "POST":
        if request.files:
            # verifico che l'upload dell'imagine è stato effettivamente eseguito
            img = request.files["image"] ##nome del file
            factor = request.form["factor"] ##valore factor per la brightness
            # controllo che venga eseguito l'upload dell'immagine
            if img.filename == "": 
                return redirect(request.url)
            # verifico che le misure siano corrette    
            if factor == 0:
                print("Inserire un valore di factor diverso da 0")
                return redirect(request.url)
            if not allowed_ext(img.filename):
                print("Estensione non supportata dal sistema")
                return redirect(request.url)

            
            img.save(os.path.join(app.config["IMAGE_UPLOADS"], img.filename))

            if username:
                print(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename)
                # Eseguo l'upload su s3 in quanto successivamente sfrutto le funzioni lamda.
                functionS3.addToBucket(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename, username+"/"+img.filename, s3, BUCKET_NAME_SATURATION)
                time.sleep(1) ##sleep per permettere il caricamento dell'immagine.
                
                # rest api lambda
                url = 'https://5f9858gv9l.execute-api.us-east-1.amazonaws.com/default/satimg?imgName='+img.filename+'&factor='+factor
                requests.get(url) ##esecuzione della rest-api
                #####

                # downloadFunction successiva per ritornare l'immagine una volta che è stata processata dalle lamda.
                #functionS3.downloadFromBucket("/home/alessio/Scrivania/Cardellini/SitoProgCardellini/Web/Functions/downloadedImages/prova.png", "prova.png", BUCKET_NAME, s3)
                return redirect(request.url)
            else:
                print(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename)
                # Eseguo l'upload su s3 in quanto successivamente sfrutto le funzioni lamda.
                functionS3.addToBucket(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename, img.filename, s3, BUCKET_NAME_SATURATION)
                time.sleep(1) ##sleep per permettere il caricamento dell'immagine.
                
                # rest api lambda
                url = 'https://5f9858gv9l.execute-api.us-east-1.amazonaws.com/default/satimg?imgName='+img.filename+'&factor='+factor
                requests.get(url) ##esecuzione della rest-api
                #####

                # downloadFunction successiva per ritornare l'immagine una volta che è stata processata dalle lamda.
                # functionS3.downloadFromBucket("/home/alessio/Scrivania/Cardellini/SitoProgCardellini/Web/Functions/downloadedImages/prova.png", "prova.png", BUCKET_NAME, s3)
                return redirect(request.url)
            
    return render_template("saturation.html")

 
@app.route('/doDownload', methods=['GET'])
def do_download():
    ##Questo metodo permette di eseguire il download dell'immagine
    global imgNameDownload

    if request.method == "GET":
        print(imgNameDownload)
        #path = app.config["IMAGE_DOWNLOADS"]+ "/sasso.png"#+imgNameDownload
        path = "/Users/alessio/SitoProgCardellini/Web/resources/imageDownload/sasso.png"
        print(path)
        return send_file(path, as_attachment=True)
            
    return render_template("download.html")



if __name__ == "__main__":
	app.run(debug = True, host='127.0.0.1', port=8080, passthrough_errors=True)
