from flask import Flask
from flask import render_template
from flask import request
import tempfile
import base64

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

# TODO: State should not be here!!
counter = 0
last_plot = (None, None)

@app.route('/')
def home():
    return render_template('home.html', count=counter, message='', lastfigure=last_plot[0], lastuser=last_plot[1])

def check_input (request, field):
    return field in request.form and len(request.form[field]) > 0


def plot_function (function, xlimits):
    def f(x):
        return eval(function)

    with tempfile.TemporaryFile() as tempf:
        t = np.arange(0.0, 10.0, 0.1)

        fig, ax = plt.subplots()
        ax.plot(t, f(t))
        ax.grid()
        ax.set_xlim(xlimits)

        fig.savefig(tempf)
        
        tempf.seek(0)
        img = tempf.read()
        return base64.b64encode(img).decode("utf-8")


@app.route('/plot', methods=['POST'])
def request_plot():
    global counter
    global last_plot

    if not check_input(request, "name") or not check_input(request, "function"):
        return render_template('home.html', count=counter, message='Invalid request: a function and a user name must be provided!') 

    name = request.form['name']
    function = request.form['function']
    
    xmin,xmax = (0,10)
    if check_input(request, "xmin"):
        try:
            xmin = float(request.form['xmin'])
        except:
            pass
    if check_input(request, "xmax"):
        try:
            xmax = float(request.form['xmax'])
        except:
            pass

    try:
        plot_base64 = plot_function (function, (xmin, xmax))

        counter = counter + 1
        last_plot = (plot_base64, name)

        return render_template('plot.html', user=name, image=plot_base64)
    except:
        return render_template('home.html', count=counter, message='Could not plot the function.') 
    


