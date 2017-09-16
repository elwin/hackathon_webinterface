import random, datetime
from flask import Flask, jsonify, render_template, send_from_directory, url_for
from functools import reduce
app = Flask(__name__)

@app.route('/')
def index():
	return jsonify(getResult())

@app.route('/dynamic')
def other():
	return render_template('hello.html')

@app.route('/static')
def alsdkjf():
	return send_from_directory('templates', 'hello.html')

# Internal Methods #

def getResult():
	slices = []
	for curTile in range(0, 16):
		slices.append(analyse(curTile))

	sliceValues = []
	for slice in slices:
		sliceValues.append(slice['values'])

	average = averageSlices(sliceValues)

	result = {
		'image_url': url_for('static', filename='image.png'),
		'contaminated': contaminated(average),
		'overall': average,
		'slices': slices,
		'slicing': {
			'x_max': 4,
			'y_max': 4
		},
		'time': datetime.datetime.now()
	}

	return result

def analyse(tile):
	slice = {
		'coordinate' : {
			'x': tile % 4,
			'y': tile / 4,
		},
		'values': getRandomValues()
	}

	return slice

def averageSlices(sliceValues):
	result = reduce(lambda x, y: {
		'clean': x['clean'] + y['clean'],
		'straw': x['straw'] + y['straw'],
		'pumpkin': x['pumpkin'] + y['pumpkin'],
		'red_beans': x['red_beans'] + y['red_beans'],
		'stones': x['stones'] + y['stones'],
		'quinoa': x['quinoa'] + y['quinoa'],
		'lentils': x['lentils'] + y['lentils'],
		'dried_bean': x['dried_bean'] + y['dried_bean'],
		'fines': x['fines'] + y['fines'],
		}, sliceValues)

	for key, value in result.items():
		result[key] = value / len(sliceValues)

	return result

def contaminated(overall):
	return overall['clean'] >= 0.1

def getRandomValues():
	values = {
		'clean': random.random(),
		'straw': random.random(),
		'pumpkin': random.random(),
		'red_beans': random.random(),
		'stones': random.random(),
		'quinoa': random.random(),
		'lentils': random.random(),
		'dried_bean': random.random(),
		'fines': random.random()
	}

	sum = 0
	for key, value in values.items():
		sum += value

	for key, value in values.items():
		values[key] = value / sum

	return values
