import kronos
import graphitesend
from django.conf import settings

PREFIX = "env_sensor"

def get_metrics_from_sensehat():

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
def send2graphite():

    g = graphitesend.init(graphite_server='localhost', prefix=PREFIX, system_name='localhost')
    if settings.DEVICE_ATTACHED == "sense_hat":
        g.send_dict(get_metrics_from_sensehat())
    if settings.DEVICE_ATTACHED == "am2302":
        g.send_dict(get_metrics_from_dht(settings.DEVICE_ATTACHED, settings.DHT_GPIO_PIN))




