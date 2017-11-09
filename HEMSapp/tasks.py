
from celery import Celery
from kombu import Queue

import subprocess
import random
import os

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HEMS.scripts.settings')

app = Celery('interface_worker', backend='amqp', broker='amqp://jessica:ASUi3dea@10.143.239.255/pi_env')

CELERY_DEFAULT_QUEUE = 'interface'
CELERY_QUEUES = (Queue('interface', routing_key='interface'),
    Queue('updater', routing_key='updater'),
    Queue('outback', routing_key='outback'),)

@app.task(name='add')
def add(x, y):
    return x + y

def create_celery_queue(queue_name):
    CELERY_QUEUES.append(Queue(queue_name, routing_key=queue_name))
    # TODO: WRITE TO A FILE OR CREATE ALL QUEUES ON START UP FROM DATABASE

def create_celery_queue_temp(queue_name):
    CELERY_QUEUES.append(Queue(queue_name, routing_key=queue_name))
    return len(CELERY_QUEUES) - 1

def remove_celery_queue(index):
    pass

@app.task(name='check_device_status')
def check_device_status(hemsID):
    #TODO: write code that determines if pi is active
    return True

def initial_handshake(hemsID):
    # step 1 create queue
    queue = create_celery_queue(hemsID)
    # step 2 add task to queue
    status = check_device_status.apply_async(args=[hemsID], queue=queue, routing_key=queue)
    # step 3 look at result / register a timeout
    tries = 0
    while status.state != 'SUCCESS':
        print status.state
        tries += 1
        time.sleep(1)
        if tries > 4:
            return False

    return True

@app.task(name='getAlle')
def getAll(inverter_id):
    # inverter = Inverter()
    # result = inverter.getAlle("0")

    print("inverter id: {0}").format(inverter_id)
    return {"inverter_id": inverter_id}
