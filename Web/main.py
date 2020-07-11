from flask import Flask, request, url_for, redirect, render_template 
#from ./Functions import imageFunctions ##import own image functions
from Functions import imageFunctions

app = Flask(__name__)

basePath = '/home/alessio/Scrivania/Cardellini/SitoProgCardellini/Web/Functions'
bewPath = '/B&W'
resizePath = '/resized'
saturationPath = '/saturation'
brightnessPath = '/brightness'
imgPath = '/images'

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

@app.route('/doResize')
def do_resize():
    print(basePath+imgPath+'/img.png')
    print(basePath+resizePath+'/prova.png')
    imageFunctions.resize(700,500, basePath+imgPath+'/img.png', basePath+resizePath+'/prova.png')
    return render_template("resizeImage.html")
 

if __name__ == "__main__":
	app.run(debug = True, host='127.0.0.1', port=8080, passthrough_errors=True)