from django.db import models

# List of supported DEVICES
SUPPORTED_DEVICES = (
    ("am2302","am2302"),
    ("dht11", "dht11"),
    ("dht22", "dht22"),
    ("sensehat", "sensehat"),
    ("rpi", "RPi")
)

# Create your models here.
# shields or attached_device

class SupportedDevices(models.Model):
    type = models.CharField(max_length=20, choices=SUPPORTED_DEVICES, unique=True)
    name = models.CharField(max_length=100)
    graphite_preffix = models.CharField(max_length=100, default="")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return '%s, %s' % (self.type, self.name)


class AttachedDevices(models.Model):
    type = models.ForeignKey(SupportedDevices)
    type = models.CharField(max_length=20, choices=SUPPORTED_DEVICES)
    name = models.CharField(max_length=100)
    graphite_preffix = models.CharField(max_length=100, default="")

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return '%s, %s' % (self.type, self.name)
