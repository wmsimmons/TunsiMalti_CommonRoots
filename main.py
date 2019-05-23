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
    db = mongo.db.lessonfiles
    entries = db.find({"$or": [
     {"tunsiMeaning": { "$regex": "%s" % word}},
     {"maltiMeaning": { "$regex": "%s" % word} },
     {"tunsiWord": { "$regex": "%s" % word} },
     {"maltiWord": { "$regex": "%s" % word} }
    ]})    
    
    return render_template('results.html', word=word, entries=entries)

@app.route('/root', methods=['GET', 'POST'])
def rootSearch():
    return render_template("/rootsearch.html")

@app.route('/category', methods=['GET', 'POST'])
def categorySearch():
    return render_template("/categorySearch.html")

@app.route('/category-results', methods=['GET', 'POST'])
def display_specific_category_results():
    word = request.args.get('searchword')
    db = mongo.db.lessonfiles
    categories = db.find({"$or": [
     {"wordCategory": { "$regex": "%s" % word}}
    ]})

    return render_template('categoryresults.html', word=word, categories=categories)

@app.route('/docs', methods=['GET', 'POST'])
def documentation():
    return render_template("/docs.html")

@app.route('/commincommon', methods=['GET', 'POST'])
def communicationInCommon():
    return render_template("/commInCommon.html")

"""MUST be at end of program | CONFIG FOR HEROKU DEPLOYMENTS"""
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
