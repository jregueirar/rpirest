import kronos
import graphitesend
from django.conf import settings



PREFIX="env_sensor.sense_hat"


def get_metrics():

    if settings.SENSE_HAT:
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
def send2graphite():

    g = graphitesend.init(graphite_server='localhost', prefix=PREFIX, system_name='')
    g.send_dict(get_metrics())


