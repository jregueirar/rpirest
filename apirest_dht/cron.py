import kronos
import graphitesend
import yaml
from unipath import Path
import logging

logger = logging.getLogger("apirest_dht")

BASE_DIR = Path(__file__).parent;
ymlconfig = BASE_DIR.child("config.yml")
with open(ymlconfig, 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

def get_metrics_from_dht(sensor_name, pin):
    import Adafruit_DHT
    sensor_args = {'dht11': Adafruit_DHT.DHT11,
                   'dht22': Adafruit_DHT.DHT22,
                   'am2302': Adafruit_DHT.AM2302}

    sensor = sensor_args[sensor_name]
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin);
    data = {}
    data['temperature'] = temperature
    data['humidity'] = humidity
    return data

@kronos.register('* * * * *')
def dhtSend2Graphite():
    if cfg['connected'] :
        for server in cfg['graphite']['servers']:
            g = graphitesend.init(graphite_server=server,  prefix='localhost.' + cfg['model'] + '.envsensor', system_name='')
            msg=g.send_dict(get_metrics_from_dht(cfg['model'], cfg['gpio']['data']))
            logger.info(msg)
