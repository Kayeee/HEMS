from django.db import models
import time

class Device(models.Model):
    #editable = 2
    name = models.CharField(max_length=100, default="Untitled Node")
    status = models.BooleanField(default=True)

    #Non-editable = 1
    created_date = models.BigIntegerField(default=time.time())

class Inverter(Device):
    pass

class Battery(Device):
    pass
