#!/bin/sh
export FLASK_APP=flaskplot.py
sudo -E python3 -m flask run -h 0.0.0.0 -p 80
