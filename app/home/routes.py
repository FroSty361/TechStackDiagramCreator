from flask import Flask, render_template
from . import home

@home.route('/')
def index():
    return render_template("home/index.html")

@home.route('/result/', methods=['GET', 'POST'])
def result():
    return render_template("home/result.html")