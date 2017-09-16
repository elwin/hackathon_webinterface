import subprocess, json, random, datetime
from flask import Flask, jsonify, render_template, send_from_directory, url_for
from functools import reduce

app = Flask(__name__)

@app.route('/')
def index():
	return send_from_directory("public", "index.html")

@app.route('/js')
def js():
	return send_from_directory("public", "buehler.js")

@app.route('/css')
def css():
	return send_from_directory("public", "style.css")

@app.route('/result')
def result():
	return jsonify(getResult())

# Internal Methods #

import random, datetime
from flask import Flask, jsonify, render_template, send_from_directory, url_for
from functools import reduce

app = Flask(__name__)

@app.route('/')
def index():
	return send_from_directory("public", "index.html")

@app.route('/js')
def js():
	return send_from_directory("public", "buehler.js")

@app.route('/css')
def css():
	return send_from_directory("public", "style.css")

@app.route('/result')
def result():
	return jsonify(getResult())

# Internal Methods #

categories = ['straw', 'stone', 'clean', 'pumpkin', 'red_beans', 'quinoa', 'lentils', 'dried_bean', 'fines']

def analyize():
	process = subprocess.Popen(['java', '-jar', 'grain.jar', 'static/image.png', '100'], stdout=subprocess.PIPE)
	return json.loads(process.stdout.read())

def prepareData(result):
	resultSet = set()

	for value in result['slices']:
		resultSet.add(value['category'])

	categoryCount = dict.fromkeys(categories)
	for key in categoryCount:
		categoryCount[key] = 0

	total = 0
	for value in result['slices']:
		categoryCount[value['category']] += 1
		total += 1

	for key, value in categoryCount.items():
		categoryCount[key] = value / float(total)

	result = {
		'categories': categories,
		'image_url': url_for('static', filename='capture.jpg'),
		'slices': result['slices'],
		'time': datetime.datetime.now(),
		'overall': categoryCount,
		'contaminated': categoryCount['clean'] >= 0.6,
		'slicing': result['slicing']
	}

	return result

def getResult():
	result = analyize()
	return prepareData(result)
