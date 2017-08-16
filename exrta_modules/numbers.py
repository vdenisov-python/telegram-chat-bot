import requests


def interesting_or_not(number):
    api_url = "http://numbersapi.com/{}/math".format(number)
    data = requests.get(api_url, params={'json': 'true'})
    info = data.json() # data.json() == json.loads(data.text)
    return info['text']
