from flask import Flask
from flask import render_template
from flask import request

import tempfile
import random

app = Flask(__name__)

# TODO Images should be listed dynamically...
def get_all_images():
    paths = ["https://www.w3schools.com/w3images/underwater.jpg",\
        "https://www.w3schools.com/w3images/ocean.jpg",\
        "https://www.w3schools.com/w3images/wedding.jpg",\
        "https://www.w3schools.com/w3images/mountainskies.jpg",\
        "https://www.w3schools.com/w3images/rocks.jpg",\
        "https://www.w3schools.com/w3images/underwater.jpg",\
        "https://www.w3schools.com/w3images/wedding.jpg",\
        "https://www.w3schools.com/w3images/rocks.jpg",\
        "https://www.w3schools.com/w3images/falls2.jpg",\
        "https://www.w3schools.com/w3images/paris.jpg",\
        "https://www.w3schools.com/w3images/nature.jpg",\
        "https://www.w3schools.com/w3images/mist.jpg",\
        "https://www.w3schools.com/w3images/paris.jpg"]

    random.shuffle(paths)
    return paths

@app.route('/newpost', methods=['GET', 'POST'])
def upload_image():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]

            with tempfile.NamedTemporaryFile() as tempf:
                image.save(tempf.name) # TODO

            return render_template('newpost.html', msg="Image uploaded!")

    return render_template('newpost.html', msg='')

@app.route('/')
def home():
    # list images to be displayed
    all_images = get_all_images()
    
    columns = [[], [], []]
    column_index = 0
    for img in all_images:
        columns[column_index].append(img)
        column_index = (column_index + 1) % 3

    return render_template('home.html', images1=columns[0], images2=columns[1], images3=columns[2])

