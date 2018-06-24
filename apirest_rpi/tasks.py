from __future__ import absolute_import, unicode_literals
from celery import shared_task
import yaml
from unipath import Path
import logging
import time

logger = logging.getLogger("apirest_rpi")

#BASE_DIR = Path(__file__).parent;
#ymlconfig = BASE_DIR.child("config.yml")
#with open(ymlconfig, 'r') as ymlfile:
#    cfg = yaml.load(ymlfile)

@shared_task
def play_audio(jobid, audiofile):
    from subprocess import call

    time.sleep(10)
    # call(["omxplayer", cfg['sounds_path'] + audiofile])
    # Change task status to completed
    #job = Job.objects.get(pk=job_id)
    #log.debug("Running job_name=%s", job.name)

    #job.status = "completed"
    #job.save()

    # Web Sockets.
    # Send status update back to browser client
    # if reply_channel is not None:
    #     Channel(reply_channel).send({
    #         "text": json.dumps ({
    #             "action": "completed",
    #             "job_id": job.id,
    #             "job_name": job.name,
    #             "job_status": job.status,
    #         })
    #     })
