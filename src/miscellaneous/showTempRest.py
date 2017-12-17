#
# Example of REST client writted in python.
# - First, it read the temperature and humidity from the am2302 sensor.
# - Last, it show the temperature and humitity in the sense-hat sensor screen
#

from unipath import Path
import requests
import yaml
import time

BASE_DIR = Path(__file__).parent
ymlconfig = BASE_DIR.child("showTempRest.yml")
with open(ymlconfig, 'r') as ymlfile:
    cfg = yaml.load(ymlfile)


def getMetricColour(name, value):
    red = {'r': 255, 'g': 0, 'b': 0}
    green = {'r': 0, 'g': 255, 'b': 0}
    yellow= {'r': 255, 'g':255, 'b':0}

    if value <= cfg[name]['thresholds']['green']:
        return green
    elif value <= cfg[name]['thresholds']['yellow']:
        return yellow
    else:
        return red

while True:
    for metric in ('temperature', 'humidity'):
        rTemp = requests.get(cfg[metric]['api'], auth=(cfg['user'], cfg['password']))
        data = rTemp.json()
        text_colour = getMetricColour(metric, data['result'])
        if metric == 'temperature':
            text_string = "T" + str(round(data['result'],1))
        else:
            text_string = "H" + str(round(data['result'],1))
        payload = {
            'back_colour': {
                'r': 0,
                'g': 0,
                'b': 0
            },
            'text_colour': text_colour,
            'text_string': text_string,
            'scroll_speed': 0.1
        }
        r = requests.put(cfg['show_message']['api'], json=payload, auth=(cfg['user'], cfg['password']))
    time.sleep(cfg['sleep_loop'])
