import kronos
import graphitesend
import yaml
from unipath import Path 
import logging

logger = logging.getLogger("apirest")

BASE_DIR = Path(__file__).parent
ymlconfig=BASE_DIR.child("config.yml")
with open(ymlconfig, 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

def get_metrics_from_sensehat():

    if cfg['connected']:
        try:
            from sense_hat import SenseHat
        except ImportError:
            raise SystemExit('[ERROR] Please make sure sense_hat is installed properly')

    sense = SenseHat()
    data = {}
    data['temperature'] = sense.get_temperature();
    data['humidity'] = sense.get_humidity();
    data['pressure'] = sense.get_pressure();

    return data;

@kronos.register('* * * * *')
def senseHatSend2Graphite():

    for server in cfg['graphite']['servers']:
        g = graphitesend.init(graphite_server=server,  prefix='localhost.' + cfg['model'] + '.envsensor', system_name='')
        msg = g.send_dict(get_metrics_from_sensehat())
        logger.info(msg)
