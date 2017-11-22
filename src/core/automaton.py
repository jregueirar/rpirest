from django.conf import settings
from sense_hat import SenseHat

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

sense = SenseHat()
sense.low_light = True
while True:
        data = get_metrics_from_dht(settings.DEVICE_ATTACHED, settings.DHT_GPIO_PIN)
        msg = "T" + str(round(data['temperature'], 1))
        msg = msg + " H" + str(round(data['humidity'], 1))
        sense.show_message(msg,text_colour=[0, 255, 0])
