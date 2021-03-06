from flask import Flask
from flask import render_template
from flask import request

import traceback
import tempfile
import time
import random
import boto3

app = Flask(__name__)

BUCKET='sdcchandson'

class Image:
    def __init__ (self, s3key, title, tags):
        self.s3key = s3key
        self.title = title
        self.tags = tags

def get_s3_bucket():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET)
    return bucket

def get_s3_fullpath(key):
    return "https://{}.s3.amazonaws.com/{}".format(BUCKET, key)

def is_image (key):  # TODO: trivial check to be improved
    return key.lower().endswith(('jpg','png','jpeg','tiff','svg'))

def get_all_images(limit = None):
    bucket = get_s3_bucket()

    images = []
    for obj in bucket.objects.all():
        if limit != None and len(images) == limit:
            break
        if not is_image(obj.key):
            continue

        images.append(Image(obj.key, "TITLE", ["tag1","tag2"])) # TODO DynamoDB

    return images

@app.route('/newpost', methods=['GET', 'POST'])
def upload_image():
    DISABLE_UPLOADING=False

    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            if not is_image(image.filename):
                return render_template('newpost.html', msg='File not valid!')

            title = ""
            tags = []

            if "title" in request.form:
                _title = request.form["title"]
                if _title != None:
                    title = _title
            if "tags" in request.form:
                _tags = request.form["tags"]
                if _tags != None:
                    tags = [t.strip() for t in _tags.split(",")]


            with tempfile.NamedTemporaryFile() as tempf:
                image.save(tempf.name)

                bucket = get_s3_bucket()

                # Construct a key
                key = ""
                if request.environ['REMOTE_ADDR'] is not None:
                    key = request.environ['REMOTE_ADDR']
                key = key + str(time.time()) + image.filename

                print("Uploading: {}".format(key))

                try:
                    if DISABLE_UPLOADING == False:
                        bucket.upload_file(tempf.name, key)

                    # TODO save metadata
                    print(title)
                    print(tags)
                except:
                    traceback.print_exc()


            return render_template('newpost.html', msg="Image uploaded!")

    return render_template('newpost.html', msg='')

@app.route('/')
def home():
    # list images to be displayed
    all_images = get_all_images(25)
    
    images = [[], [], []]
    column_index = 0
    for img in all_images:
        imgpath = get_s3_fullpath(img.s3key)
        if len(img.tags) != 0:
            tagsstring = "[{}]".format(",".join(img.tags))
        else:
            tagsstring = ""

        images[column_index].append((imgpath, img.title, tagsstring))
        column_index = (column_index + 1) % 3

    print(images)
    return render_template('home.html', images1=images[0], images2=images[1], images3=images[2])
