import subprocess, json

def analyize():
    process = subprocess.Popen(['java', '-jar', 'grain.jar', 'static/image.png', '100'], stdout=subprocess.PIPE)
    return json.loads(process.stdout.read())

def prepareData(result):
    resultSet = set()

    for value in result['slices']:
        resultSet.add(value['category'])

    categories = list(resultSet)

    categoryCount = dict.fromkeys(categories)
    for key in categoryCount:
        categoryCount[key] = 0

    total = 0
    for value in result['slices']:
        categoryCount[value['category']] += 1
        total += 1

    for key, value in categoryCount.items():
        categoryCount[key] = value / total

    result = {
        'categories': categories,
        #'image_url': url_for('static', filename='capture.jpg'),
        'slices': result['slices'],
        'time': datetime.datetime.now(),
        'overall': categoryCount,
        'contaminated': categoryCount['clean'] >= 0.6
    }

    return jsonify(result)
