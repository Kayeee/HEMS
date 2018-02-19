
from celery import Celery
from kombu import Queue

import subprocess
import random
import os
import requests
import time
import logging
import sys
import json
import socket
import fcntl
import struct


app = Celery('interface_worker', backend='amqp', broker='amqp://Kevin:ASUi3dea@127.0.0.1/pi_env')
queue_number_str = '1'
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

@app.task(name='readValue')
def readValue(device_name):
    path = "HEMS/project/wrapper_python"
    os.chdir(path)
    result = subprocess.Popen(["python", "read_outback.py", device_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err=result.communicate()
    if result.returncode != 0:
        raise OSError("covert error")
    return out

@app.task(name='writeValue')
def writeValue(device_name, value):
    path = "HEMS/project/wrapper_python"
    os.chdir(path)
    result = subprocess.Popen(["python", "write_outback.py", device_name, value], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err=result.communicate()
    if result.returncode != 0:
        raise OSError("covert error")
    return out

def getOutBackResult(hems_device, hems_method, hems_value):
    # step 1 create queue
    #queue = create_celery_queue("1")
    # step 2 add task to queue
    if hems_method=="read":
        # assign pi to do the tasks
        return getReadValue(hems_device)
    elif hems_method=="write":
        # assign pi to do the tasks
        return getWriteValue(hems_device, hems_value)

def getOutBackCommandResult(hems_command):
    words = hems_command.split()
    method = words[0]
    if method == "read":
        if check_read_words(words):
            return getReadValue(words[1])
        else:
            return "Please check your command line"
    elif method == "write":
        if check_write_words(words):
            return getWriteValue(words[1], words[2])
        else:
            return "Please check your command line"
    else:
        return "Please check your command line!"

# Helper Method #
def getReadValue(hems_device):
    result = readValue.apply_async(args=[hems_device], queue=queue_number_str,routing_key=queue_number_str)
    tries = 0
    while result.status != 'SUCCESS':
        print(result.status)
        tries += 1
        time.sleep(1)
        if tries > 100:
            return "Cannot get result."
    # receive result from pi
    received_result = result.get()
    print(received_result)
    return received_result

def getWriteValue(hems_device, hems_value):
    result = writeValue.apply_async(args=[hems_device, hems_value], queue=queue_number_str,routing_key=queue_number_str)
    tries = 0
    while result.status != 'SUCCESS':
        print(result.status)
        tries += 1
        time.sleep(1)
        if tries > 100:
            return "Cannot get result"
    # receive result from pi
    received_result = result.get()
    print(received_result)
    return received_result

def check_read_words(words):
    if len(words) != 2:
        return False
    return True

def check_write_words(words):
    if len(words) != 3:
        return False
    return True

# Test Method #
@app.task(name='runCommand')
def run_command(x, y):
    os.chdir("HEMS/project/wrapper_python")
    result = subprocess.Popen(["python", "test1.py", str(x), str(y)], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = result.communicate()
    if result.returncode != 0:
        print("stderr: [%s]" % err)
        print("stdout: [%s]" % out)
    return out

def getResult(x, y):
    # step 1 create queue_name
    #queue = create_celery_queue("1")
    result = run_command.apply_async(args=[x,y], queue=queue_number_str, routing_key=queue_number_str)
    tries = 0
    while result.status != "SUCCESS":
        print(result.status)
        tries += 1
        time.sleep(1)
        if tries > 100:
            return "Cannot get result."
    return result.get()

def getHEMSResult(device, method):
    result = device + method
    return result
