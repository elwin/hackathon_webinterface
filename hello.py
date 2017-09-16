import subprocess, json, random, datetime
from flask import Flask, jsonify, render_template, send_from_directory, url_for
from functools import reduce
from picamera import PiCamera
from time import sleep

camera = PiCamera()

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


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

# Internal Methods #

categories = ['straw', 'stone', 'clean', 'pumpkin', 'red_beans', 'quinoa', 'lentils', 'dried_bean', 'fines']

def analyize():
	process = subprocess.Popen(['java', '-jar', 'grain.jar', 'static/capture.jpg', '25'], stdout=subprocess.PIPE)
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
		'contaminated': categoryCount['clean'] < 0.8,
		'slicing': result['slicing']
	}

	return result

def getResult():
	camera.capture('/home/pi/web/static/capture.jpg')
	result = analyize()
	return prepareData(result)import subprocess, json, random, datetime
from flask import Flask, jsonify, render_template, send_from_directory, url_for
from functools import reduce
from picamera import PiCamera
from time import sleep

camera = PiCamera()

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


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

# Internal Methods #

categories = ['straw', 'stone', 'clean', 'pumpkin', 'red_beans', 'quinoa', 'lentils', 'dried_bean', 'fines']

def analyize():
	process = subprocess.Popen(['java', '-jar', 'grain.jar', 'static/capture.jpg', '25'], stdout=subprocess.PIPE)
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
		'contaminated': categoryCount['clean'] < 0.8,
		'slicing': result['slicing']
	}

	return result

def getResult():
	camera.capture('/home/pi/web/static/capture.jpg')
	result = analyize()
	return prepareData(result)