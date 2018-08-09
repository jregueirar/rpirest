from __future__ import absolute_import, unicode_literals
from celery import shared_task
import yaml
from unipath import Path
import logging
import time



logger = logging.getLogger("apirest_rpi")

BASE_DIR = Path(__file__).parent;
ymlconfig = BASE_DIR.child("config.yml")
with open(ymlconfig, 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

# Syncing info of Job with AsyncResult
@shared_task
def sync_job_db(job_id):

   job = Job.objects.get(pk=job_id)
   res = AsyncResult(job.celery_id)
   res.result
   #job.completed = res._cache['date_done']
   job.status = res.status
   job.save()

@shared_task
def play_audio(audiofile):
    from subprocess import call

    #log.debug("job Name=%s", data['job_name'])

    time.sleep(2)

    # call(["omxplayer", cfg['sounds_path'] + audiofile])


    #call(["omxplayer", cfg['sounds_path'] + audiofile])
    #Change task status to completed
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

    # Save model to our database
    #job = Job(
    #    name=data['job_name'],
    #    status="started",
    #)
    #job.save()

    # Start long running task here (using Celery)
    #sec3_task = sec3.delay(job.id, reply_channel)

    # Store the celery task id into the database if we wanted to
    # do things like cancel the task in the future
    #job.celery_id = sec3_task.id
    #job.save()
