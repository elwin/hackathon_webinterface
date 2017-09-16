import random, datetime
from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/')
def index():

    slices = []
    for curTile in range(0, 16):
        slices.append(analyse(curTile))

    average = averageSlices(slices)

    result = {
        'contaminated': contaminated(average),
        'overall': average,
        'slices': slices,
        'slicing': {
            'x_max': 4,
            'y_max': 4
        },
        'time': datetime.datetime.now()
    }

    return jsonify(result)


def analyse(tile):
    slice = {
        'coordinate' : {
            'x': tile,
            'y': tile,
        },
        'clean': 0.5,
        'quinoa': 0.2,
        'straw': 0.1,
        'wheat': 0.2
    }

    return slice

def averageSlices(slices):
    result = reduce(lambda x, y: {
        'clean': x['clean'] + y['clean'],
        'quinoa': x['quinoa'] + y['quinoa'],
        'wheat': x['wheat'] + y['wheat'],
        'straw': x['straw'] + y['straw'],
        }, slices)

    for key, value in result.items():
        result[key] = value / len(slices)

    return result

def contaminated(overall):
    return overall['clean'] >= 0.5
