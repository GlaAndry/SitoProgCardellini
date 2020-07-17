##flask import
from flask import Flask, request, url_for, redirect, render_template, send_file
from Functions import imageFunctions

##import external resources
from aws import functionS3
from aws import configS3
from aws import functionCognito
from aws import functionDynamo

##aws boto3 import
import boto3
from botocore.client import Config

#os import
import time
import requests
import os


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

# app config paths
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

s3_client = boto3.client('s3',
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
    print(nomeUtente)
    return render_template("index.html", results = nomeUtente)


@app.route('/signin')
def signin():
    return render_template("signin.html")

@app.route('/logout')
def logout():
    return render_template("logout.html")

@app.route('/doLogout', methods=['GET', 'POST'])
def do_logout():
    ##inizializzo la varibaile nomeutente per eseguire il logout
    global nomeUtente
    nomeUtente = ""
    return render_template("logout.html")


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

            return render_template("accediOK.html", results = nomeUtente)

        except Exception as e:
            print(e)
            return render_template("accessoNegato.html")



    return render_template("signin.html")



@app.route('/tableImageForUser')
def tableImageForUser():
    return render_template("tableImageForUser.html", results2 = nomeUtente)


@app.route('/doListTable', methods=['GET', 'POST'])
def do_list_table():
    
    userImg = []
    fieldnames = []
    global nomeUtente
    ##verifico che ci sia un evento di post
    if request.method == "POST":
        
        ##Tramite dynamoDB vado ad eseguire una select sul nomeUtente.
        userImg = functionDynamo.get_element_from_table(dynamodb,"Utenti", nomeUtente)
        if not nomeUtente:
            return render_template('tableUserNotRegistred.html')
        elif not userImg:
            return render_template('tableEmptyUser.html', results2 = nomeUtente)
        else:
            for link in userImg:
                funzione = determineFunction(link.get('link')) ##determino la funzione eseguita dal sistema
                iName = retrieve_nome_from_link(link.get('link')) ##determino il nome dell'immagine
                ##aggiungo la funzione eseguita nel ritorno 
                ##(userImg è una lista di dizionari, per questo è stata possibile l'associazione)
                link['funzione'] = funzione
                link['nomeImmagine'] = iName[4]  ##Prendo la posizione 4 in base al parsing del link s3 fornito
            return render_template('tableImageForUser.html', results=userImg, fieldnames=fieldnames, len=len, results2 = nomeUtente)



    return render_template("tableImageForUser.html")

@app.route('/resizeImage')
def resizeImage():
    return render_template("resizeImage.html", results = nomeUtente)


@app.route('/black_and_white')
def black_and_white():
    return render_template("blackAndWhite.html", results = nomeUtente)


@app.route('/saturation')
def saturation():
    return render_template("saturation.html", results = nomeUtente)


@app.route('/brightness')
def brightness():
    return render_template("brightness.html", results = nomeUtente)


@app.route('/links')
def links():
    return render_template("link.html", results = nomeUtente)


@app.route('/doBeW', methods=['GET','POST'])
def doBeW():
    # blackAndWhite image

    username = nomeUtente
    #global imgNameDownload


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

            #Salvo l'immagine in loacale.
            img.save(os.path.join(app.config["IMAGE_UPLOADS"], img.filename))

            if username:
                print(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename)
                # Eseguo l'upload su s3 in quanto successivamente sfrutto le funzioni lamda.
                functionS3.addToBucket(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename, username+"/"+img.filename, s3, BUCKET_NAME_BeW)
                # rest api lambda
                url = 'https://3fsi3za5x1.execute-api.us-east-1.amazonaws.com/default/bewImg?&imgName='+img.filename
                requests.get(url) ##esecuzione della rest-api
                #Download dal bucket S3 dell'immagine, una volta che è stata processata dalla lamda.
                functionS3.downloadFromBucket(os.path.join(app.config["IMAGE_DOWNLOADS"])+"/"+img.filename, username+"/"+img.filename, BUCKET_NAME_BeW, s3)
                ##Inserisco gli elementi all'interno di DynamoDB -->{Nome Utente, linkS3}
                urlS3 = "https://%s.s3.amazonaws.com/%s/%s" % (configS3.S3_BUCKET_BeW, username, img.filename)
                functionDynamo.add_element_in_table(dynamodb, "Utenti", username, urlS3)
                #rendo il nome dell'immagine globale per il successivo utilizzo nel download.
                global imgNameDownload
                imgNameDownload = img.filename
                #Eseguo il download.
                return redirect(url_for('do_download'))

            else:
                print(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename)
                # Eseguo l'upload su s3 in quanto successivamente sfrutto le funzioni lamda.
                functionS3.addToBucket(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename, img.filename, s3, BUCKET_NAME_BeW)                
                # rest api lambda
                url = 'https://3fsi3za5x1.execute-api.us-east-1.amazonaws.com/default/bewImg?&imgName='+img.filename
                requests.get(url) ##esecuzione della rest-api
                #Download dal bucket S3 dell'immagine, una volta che è stata processata dalla lamda.
                functionS3.downloadFromBucket(os.path.join(app.config["IMAGE_DOWNLOADS"])+"/"+img.filename, img.filename, BUCKET_NAME_BeW, s3)
                imgNameDownload = img.filename
                #Eseguo il download.
                return redirect(url_for('do_download'))
    else:
        return render_template("blackAndWhite.html")

    return render_template("blackAndWhite.html")


@app.route('/doResize', methods=['GET','POST'])
def do_resize():
    # resize image

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

            
            #Salvo l'immagine in locale.
            img.save(os.path.join(app.config["IMAGE_UPLOADS"], img.filename))

            if username:
                print(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename)
                # Eseguo l'upload su s3 in quanto successivamente sfrutto le funzioni lamda.
                functionS3.addToBucket(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename, username+"/"+img.filename, s3, BUCKET_NAME_RESIZE)                
                # rest api lambda
                url = 'https://62j41asgt0.execute-api.us-east-1.amazonaws.com/default/resImg?wSize='+wSize+'&hSize='+hSize+'&imgName='+img.filename
                requests.get(url) ##esecuzione della rest-api
                #Download dal bucket S3 dell'immagine, una volta che è stata processata dalla lamda.
                functionS3.downloadFromBucket(os.path.join(app.config["IMAGE_DOWNLOADS"])+"/"+img.filename, username+"/"+img.filename, BUCKET_NAME_RESIZE, s3)
                ##Inserisco gli elementi all'interno di DynamoDB -->{Nome Utente, linkS3}
                urlS3 = "https://%s.s3.amazonaws.com/%s/%s" % (configS3.S3_BUCKET_RESIZE, username, img.filename)
                functionDynamo.add_element_in_table(dynamodb, "Utenti", username, urlS3)
                #rendo il nome dell'immagine globale per il successivo utilizzo nel download.
                global imgNameDownload
                imgNameDownload = img.filename
                #Eseguo il download.
                return redirect(url_for('do_download'))
            else:
                print(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename)
                # Eseguo l'upload su s3 in quanto successivamente sfrutto le funzioni lamda.
                functionS3.addToBucket(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename, img.filename, s3, BUCKET_NAME_RESIZE)                
                # rest api lambda
                url = 'https://62j41asgt0.execute-api.us-east-1.amazonaws.com/default/resImg?wSize='+wSize+'&hSize='+hSize+'&imgName='+img.filename
                requests.get(url) ##esecuzione della rest-api
                #Download dal bucket S3 dell'immagine, una volta che è stata processata dalla lamda.
                functionS3.downloadFromBucket(os.path.join(app.config["IMAGE_DOWNLOADS"])+"/"+img.filename, img.filename, BUCKET_NAME_RESIZE, s3)
                imgNameDownload = img.filename
                #Eseguo il download.
                return redirect(url_for('do_download'))
            
    return render_template("resizeImage.html")


@app.route('/doBrightness', methods=['GET','POST'])
def do_brightness():
    # brightness image

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
                # rest api lambda
                url = 'https://jx902kdqgc.execute-api.us-east-1.amazonaws.com/default/brightnessimg?imgName='+img.filename+'&factor='+factor
                requests.get(url) ##esecuzione della rest-api
                #Download dal bucket S3 dell'immagine, una volta che è stata processata dalla lamda.
                functionS3.downloadFromBucket(os.path.join(app.config["IMAGE_DOWNLOADS"])+"/"+img.filename, username+"/"+img.filename, BUCKET_NAME_BRIGHTNESS, s3)
                ##Inserisco gli elementi all'interno di DynamoDB -->{Nome Utente, linkS3}
                urlS3 = "https://%s.s3.amazonaws.com/%s/%s" % (configS3.S3_BUCKET_BRIGHTNESS, username, img.filename)
                functionDynamo.add_element_in_table(dynamodb, "Utenti", username, urlS3)
                #rendo il nome dell'immagine globale per il successivo utilizzo nel download.
                global imgNameDownload
                imgNameDownload = img.filename
                #Eseguo il download.
                return redirect(url_for('do_download'))
            else:
                print(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename)
                # Eseguo l'upload su s3 in quanto successivamente sfrutto le funzioni lamda.
                functionS3.addToBucket(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename, img.filename, s3, BUCKET_NAME_BRIGHTNESS)                
                # rest api lambda
                url = 'https://jx902kdqgc.execute-api.us-east-1.amazonaws.com/default/brightnessimg?imgName='+img.filename+'&factor='+factor
                requests.get(url) ##esecuzione della rest-api
                #Download dal bucket S3 dell'immagine, una volta che è stata processata dalla lamda.
                functionS3.downloadFromBucket(os.path.join(app.config["IMAGE_DOWNLOADS"])+"/"+img.filename, img.filename, BUCKET_NAME_BRIGHTNESS, s3)
                imgNameDownload = img.filename
                #Eseguo il download.
                return redirect(url_for('do_download'))
            
    return render_template("brightness.html")


@app.route('/doSaturation', methods=['GET','POST'])
def do_saturation():
    # saturation image
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
                # rest api lambda
                url = 'https://5f9858gv9l.execute-api.us-east-1.amazonaws.com/default/satimg?imgName='+img.filename+'&factor='+factor
                requests.get(url) ##esecuzione della rest-api
                #Download dal bucket S3 dell'immagine, una volta che è stata processata dalla lamda.
                functionS3.downloadFromBucket(os.path.join(app.config["IMAGE_DOWNLOADS"])+"/"+img.filename, username+"/"+img.filename, BUCKET_NAME_SATURATION, s3)
                ##Inserisco gli elementi all'interno di DynamoDB -->{Nome Utente, linkS3}
                urlS3 = "https://%s.s3.amazonaws.com/%s/%s" % (configS3.S3_BUCKET_SATURATION, username, img.filename)
                functionDynamo.add_element_in_table(dynamodb, "Utenti", username, urlS3)
                #rendo il nome dell'immagine globale per il successivo utilizzo nel download.
                global imgNameDownload
                imgNameDownload = img.filename
                #Eseguo il download.
                return redirect(url_for('do_download'))
            else:
                print(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename)
                # Eseguo l'upload su s3 in quanto successivamente sfrutto le funzioni lamda.
                functionS3.addToBucket(os.path.join(app.config["IMAGE_UPLOADS"])+"/"+img.filename, img.filename, s3, BUCKET_NAME_SATURATION)                
                # rest api lambda
                url = 'https://5f9858gv9l.execute-api.us-east-1.amazonaws.com/default/satimg?imgName='+img.filename+'&factor='+factor
                requests.get(url) ##esecuzione della rest-api
                #Download dal bucket S3 dell'immagine, una volta che è stata processata dalla lamda.
                functionS3.downloadFromBucket(os.path.join(app.config["IMAGE_DOWNLOADS"])+"/"+img.filename, img.filename, BUCKET_NAME_BRIGHTNESS, s3)
                imgNameDownload = img.filename
                #Eseguo il download.
                return redirect(url_for('do_download'))
            
    return render_template("saturation.html")

 
@app.route('/doDownload', methods=['GET'])
def do_download():
    ##Questo metodo permette di eseguire il download dell'immagine
    global imgNameDownload

    if request.method == "GET":
        pathImg = app.config["IMAGE_DOWNLOADS"]+"/"+imgNameDownload
        return send_file(pathImg, as_attachment=True)

    return render_template("download.html")


@app.route('/doDownloadFromUrl', methods=['POST'])
def do_download_from_url():
    ##Questo metodo permette di eseguire il download dell'immagine
    if request.method == "POST":
        ##Ricavo il link dalla form html.
        s3Link = request.form['urlButton']
        ##Eseguo il parsing del link.
        imgNameDown, bucktN = parse_s3_link(s3Link) ## [0] --> email , [1]--> bucketName
        ##genero il path della cartella per una eventuale creazione.
        emailName = imgNameDown.split("/",1)
        path = app.config["IMAGE_DOWNLOADS"]+"/"+emailName[0]
        ##Creo la cartella in locale nella quale scaricare il file.
        try:
            os.mkdir(path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s " % path)

        ##Eseguo il download da s3.
        functionS3.downloadFromBucket(os.path.join(app.config["IMAGE_DOWNLOADS"])+"/"+imgNameDown, imgNameDown, bucktN[0], s3)
        pathImg = app.config["IMAGE_DOWNLOADS"]+"/"+imgNameDown
        print(pathImg)
        ##Eseguo il download per l'utente.
        return send_file(pathImg, as_attachment=True)
            
    return render_template("download.html")


def parse_s3_link(link):
    ##Questo metodo va ad eseguire il parsing del link di s3
    bucket, key = link.split('/',2)[-1].split('/',1)
    bucket_n = bucket.split('.',1)

    return key, bucket_n

def retrieve_nome_from_link(link):
    ##Questo metodo va a ricavare il nome dell'immagine 
    ##dal link di s3 fornito.
    nomeImmagine = link.split("/", 4)
    return nomeImmagine

def determineFunction(str):
    #Attraverso questa funzione eseguiamo il parsing del nome del bucket
    #Per determinare che tipologia di funzione è associata
    fun = ""
    if str.find("resize") != -1:
        fun = "Resize"
    elif str.find("brightness") != -1:
        fun = "Brightness"
    elif str.find("blackwhite") != -1:
        fun = "Black And White"
    else:
        fun = "Saturation"
    return fun

if __name__ == "__main__":
	app.run(debug = True, host='127.0.0.1', port=8080, passthrough_errors=True)
