from flask import Flask, render_template , request
from . import home
import datetime as dt

@home.route('/')
def index():
    return render_template("home/index.html")

@home.route('/result/', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        githubURL = request.form['githubURL']

        print(githubURL)

        return render_template("home/result.html")

    return render_template("home/result.html")

@home.route('/logs/')
def logs_iframe():
    time = dt.datetime.now()

    timeStr = time.strftime("%H:%M:%S")

    return render_template("home/iframe-logs.html", time=timeStr, logs=["Hi!", "Mesmeizer", "Sakuya Uses Pads"])