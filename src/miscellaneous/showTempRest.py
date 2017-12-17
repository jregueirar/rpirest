from unipath import Path
import requests
import yaml
import json

BASE_DIR = Path(__file__).parent
ymlconfig = BASE_DIR.child("showTempRest.yml")
with open(ymlconfig, 'r') as ymlfile:
    cfg = yaml.load(ymlfile)


def getMetricColour(name, value):
    red=(255,0,0)
    green=(0,255,0)
    yellow=(255, 255, 0)

    if value <= cfg[name]['green']:
        return green
    elif value <= cfg[name]['yellow']:
        return yellow
    else:
        return red


rTemp = requests.get(cfg['temperature']['api'], auth=(cfg['user'], cfg['password']))
data = rTemp.json()
print(data['result'])

rTemp = requests.get(cfg['humidity']['api'], auth=(cfg['user'], cfg['password']))
data = rTemp.json()
print(data)

message=[]
payload = {
    'back_colour': {
        'r': 0,
        'g': 0,
        'b': 0
    },
    'text_colour': {
        'r': 255,
        'g': 0,
        'b': 0
    },
    'text_string': "Hola",
    'scroll_speed': 0.07
}

string = json.dumps(payload)
print(string)
r = requests.put(cfg['show_message']['api'], json=payload, auth=(cfg['user'], cfg['password']))
print(r.status_code)
print(r.headers)
