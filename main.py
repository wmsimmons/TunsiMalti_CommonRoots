#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, flash
from flask_bootstrap import Bootstrap
from flask import render_template, request, url_for
from flask_pymongo import PyMongo
import os

#command to run app locally C:\Python34 .\python.exe C:\Users\langu\Desktop\qafasTaMalti\sanna\sannadictsite\main.py

app = Flask(__name__)
Bootstrap(app)

"""for the app and mongo configs"""
app.config['SECRET_KEY'] = '3bjd&hdj3%7@hdmSAN&**NA&**DICT&**%$324d'
app.config['MONGO_DBNAME'] = 'langilsna'
app.config['MONGO_URI'] = 'mongodb://tunsimalti:tunsimalti1@ds133166.mlab.com:33166/langilsna'
# end of app configs for PyMongo

mongo = PyMongo(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("/index.html")

@app.route('/word/<word>', methods=['GET', 'POST'])
def wordDisplay(word):
    result = request.args.get('searchword')
    db = mongo.db.lessonfiles
    entry = db.find_one({"tunsiMeaning":word}) or db.find_one({"maltiMeaning":word}) or db.find_one({"tunsiWord":word}) or db.find_one({"maltiWord":word})
    return render_template('word.html', word=word, entry=entry, result=result)

@app.route('/results', methods=['GET', 'POST'])
def resultDisplay():
    word = request.args.get('searchword')
    return render_template('results.html', word=word)


"""MUST be at end of program"""
if __name__ == '__main__':
    app.run(debug=True)	