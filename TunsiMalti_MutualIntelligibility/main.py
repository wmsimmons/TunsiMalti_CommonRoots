#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, flash
from flask_bootstrap import Bootstrap
from flask import render_template, request, url_for, jsonify
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

"""
"""
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

@app.route('/category', methods=['GET', 'POST'])
def categorySearch():
    category = request.args.get('categories')
    db = mongo.db.lessonfiles
    categories = db.find({}, {"wordCategory": 1, "_id": 0})
    a = db.find({"wordCategory": category})

    return render_template("/categorySearch.html", categories=categories, a=a)

@app.route('/category-results/<category>', methods=['GET', 'POST'])
def display_specific_category_results(category):
    word = request.args.get('categories')
    db = mongo.db.lessonfiles
    category_word_results = db.find({"wordCategory": category})

    return render_template('categoryresults.html', word=word, category_word_results=category_word_results, category=category)

@app.route('/docs', methods=['GET'])
def documentation():
    return render_template("/docs.html")

@app.route('/commincommon', methods=['GET'])
def communicationInCommon():
    return render_template("/commInCommon.html")

@app.route('/root', methods=['GET', 'POST'])
def rootSearch():
    return render_template("/rootsearch.html")

"""         API SECTION      """
# displays a rest api page that displays all db words
@app.route('/allwords', methods=['GET'])
def get_all_words():
    all_words = mongo.db.lessonfiles
    output = []
    
    for query in all_words.find({"lemmaId":""}):
        str_id = str(query['_id'])
        output.append({"_id": str_id,
                    "tunsiMeaning": query['tunsiMeaning'],
                    "maltiMeaning": query['maltiMeaning'],
                    "tunsiWord": query['tunsiWord'],
                    "maltiWord": query['maltiWord']})

    return jsonify({'result': output})

# displays a rest api page that displays words by specific categories
@app.route('/allwordsbycat/<category>', methods=['GET'])
def get_all_words_by_category(category):
    all_words = mongo.db.lessonfiles
    query_for_category = all_words.find({"wordCategory": category})

    output = []

    if query_for_category:
        for query in query_for_category:
            output.append({"tunsiMeaning": query['tunsiMeaning'],
                        "maltiMeaning": query['maltiMeaning'],
                        "tunsiWord": query['tunsiWord'],
                        "maltiWord": query['maltiWord'],
                        "wordCategory": query['wordCategory']})
    else:
        output = 'No results found.'

    return jsonify({'result': output})

# as a user, i'd like to filter results on api page for categories
# as a user, id like to edit (put) any attribute or delete any entry
# as a user, id like to add some entry

"""   END OF API SECTION     """


"""MUST be at end of program | CONFIG FOR HEROKU DEPLOYMENTS"""
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)	
