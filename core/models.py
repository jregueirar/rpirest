from django.db import models
from django.utils import timezone

# Create your models here.
class Job(models.Model):
    name = models.CharField(max_length=255)                             # Name of the task
    #status = models.CharField(max_length=255, null=True, blank=True)    # Redundant info, in Asyncresult.
    created = models.DateTimeField(default=timezone.now)
    #completed = models.DateTimeField(null=True, blank=True)             # Redundant info, in Asyncresult.
    celery_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return self.name
