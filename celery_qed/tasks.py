"""
QED celery instance
"""

import os
import logging
import redis
from celery import Celery

logging.getLogger('celery.task.default').setLevel(logging.DEBUG)
logging.getLogger().setLevel(logging.DEBUG)

redis_hostname = os.environ.get('REDIS_HOSTNAME')
redis_port = os.environ.get('REDIS_PORT')
REDIS_HOSTNAME = os.environ.get('REDIS_HOSTNAME')

if not os.environ.get('REDIS_HOSTNAME'):
    os.environ.setdefault('REDIS_HOSTNAME', 'localhost')
    REDIS_HOSTNAME = os.environ.get('REDIS_HOSTNAME')

logging.info("REDIS HOSTNAME: {}".format(REDIS_HOSTNAME))

redis_conn = redis.StrictRedis(host=REDIS_HOSTNAME, port=6379, db=0)

app = Celery('tasks',
             broker='redis://{}:6379/0'.format(REDIS_HOSTNAME),
             backend='redis://{}:6379/0'.format(REDIS_HOSTNAME))

app.conf.update(
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
)

# ------ SAM ------ #
from ubertool_ecorest.REST_UBER import rest_model_caller
from ubertool_ecorest.ubertool.ubertool.sam import sam_exe as sam


@app.task(bind=True)
def sam_run(session_id, session_inputs):
    logging.info("celery_qed received inputs: {}".format(session_inputs))
    logging.info("sam starting...")
    rest_model_caller.model_run("sam", session_id, session_inputs, module=sam)


@app.task
def sam_status(session_id):
    logging.info("celery_qed received request for sam status")
    logging.info("checking status of sam task: " + session_id)
    task = app.AsyncResult(session_id)
    logging.info("sam task status" + task.status)
    return {"status": task.status}
