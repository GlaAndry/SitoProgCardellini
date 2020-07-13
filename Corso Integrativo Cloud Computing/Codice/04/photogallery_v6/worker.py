from flask import Flask
from flask import request, Response

from awscommon import *

import base64
import imageutils
import tempfile
import boto3

application = Flask(__name__)

def apply_filter (key, filtername):
    filters = []

    if filtername == "(None)":
        pass
    elif filtername == "Black and White" or filtername == "bw":
        filters.append(filtername)
    elif filtername == "Blur":
        filters.append(filtername)
    else:
        print("Invalid filter: {}".format(filtername))

    max_size = 900
    with tempfile.NamedTemporaryFile() as tempf:
        s3 = boto3.client('s3')
        bucket = get_s3_bucket()
        fullkey = "pending/{}".format(key)
        s3.download_file(BUCKET, fullkey, tempf.name)
        imageutils.apply_filters(tempf.name, filters, max_size)
        boto3.resource('s3').Object(BUCKET, fullkey).delete()
        bucket.upload_file(tempf.name, key)

    


@application.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return Response("", status=200)

    msg = base64.b64decode(request.data)
    msgstring = msg.decode('ascii')
    key,filtername = msgstring.split('\n')

    #raise ValueError("{}; {}".format(key, filtername))
    apply_filter(key, filtername)

    return Response("", status=200)

if __name__ == "__main__":
    application.run(host='0.0.0.0')
