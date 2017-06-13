
from celery import Celery
from kombu import Queue

import subprocess
import random
import os

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HEMS.scripts.settings')

app = Celery('interface_worker', backend='amqp', broker='amqp://Kevin:ASUi3dea@52.87.223.187/pi_env')

CELERY_DEFAULT_QUEUE = 'interface'
CELERY_QUEUES = (Queue('interface', routing_key='interface'),
    Queue('updater', routing_key='updater'),
    Queue('outback', routing_key='outback'),)

@app.task(name='getAlle')
def getAll(inverter_id):
    # inverter = Inverter()
    # result = inverter.getAlle("0")

    print("inverter id: {0}").format(inverter_id)
    return {"inverter_id": inverter_id}
