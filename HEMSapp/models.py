from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db.models.signals import *

import time


######################## User Info ##########################



class HemsUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password):
        """
        Creates and saves a User with the given email, and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('User must have a first_name')
        if not last_name:
            raise ValueError('User must have a last_name')
        if not last_name:
            raise ValueError('User must have a last_name')
        if not password:
            raise ValueError('User must have a password')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            password=password,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password):
        """
        Creates and saves a superuser with the given email, and password.
        """
        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user



class HemsUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    objects = HemsUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'first_name', 'last_name']

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class Address(models.Model):
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    zipCode = models.IntegerField()

    def format(self):
        return self.street1 + "\n" + self.street2 + "\n" + self.city + ", " + self.state + " " + str(self.zip)

    class Meta:
        verbose_name = "Address"


###################### Devices ##########################
#our HEMS box
class HemsBox(models.Model):
    #hemsID is our version of a serial number for the box
    hemsID = models.CharField(max_length=40, default="NoIdEstablished")
    owner = models.OneToOneField(HemsUser, on_delete=models.CASCADE, related_name='hemsbox_set')


#Devices attached to HEMS box are called "assets"
class Asset(models.Model):
    #editable
    name = models.CharField(max_length=100, default="Untitled Node")
    status = models.BooleanField(default=True)
    hems_box = models.ForeignKey(HemsBox, on_delete=models.CASCADE)
    manufacturer = models.CharField(max_length=40, default="N/A")

    #Non-editable
    created_date = models.BigIntegerField(default=time.time())

    class Meta:
        abstract = True

#Asset Subclasses
class SolarPV(Asset):
    #Information Unique to a SolarPV

    class Meta:
        default_related_name = 'solarPV_set'

class Inverter(Asset):
    #Information Unique to a Inverter

    class Meta:
        default_related_name = 'inverter_set'

class Grid(Asset):
    #Information Unique to a Grid

    class Meta:
        default_related_name = 'grid_set'

class Load(Asset):
    #Information Unique to a Load

    class Meta:
        default_related_name = 'load_set'

class Battery(Asset):
    #Information Unique to a Battery

    class Meta:
        default_related_name = 'battery_set'


########################### Data Objects ####################
class HemsData(models.Model):
    value = models.FloatField(default=-1)
    timestamp = models.DateTimeField(auto_now_add=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        unique_together   = ('content_type', 'object_id')
        abstract = True

class IncidentRadiation(HemsData):
    unit = "W/m^2"
    unit_verbose = "Watts per Meter Squared"

    class Meta:
        default_related_name = 'incident_radiatioin_set'


class DCPower(HemsData):
    unit = "kW"
    unit_verbose = "Kilowatt"

    class Meta:
        default_related_name = 'dc_power_set'

class Energy(HemsData):
    unit = "kWh"
    unit_verbose = "Kilowatt Hours"

    class Meta:
        default_related_name = 'energy_set'

class Voltage(HemsData):
    unit = "V"
    unit_verbose = "Volts"

    class Meta:
        default_related_name = 'voltage_set'

class Current(HemsData):
    unit = "A"
    unit_verbose = "Amps"

    class Meta:
        default_related_name = 'current_set'

class ACPower(HemsData):
    unit = "kW"
    unit_verbose = "Kilowatt Hours"

    class Meta:
        default_related_name = 'ac_power_set'

class ReactivePower(HemsData):
    unit = "Vars"
    unit_verbose = ""

    class Meta:
        default_related_name = "related_power_set"

class DCACEfficiency(HemsData):
    unit = "%%"
    unit_verbose = "Percent"

    class Meta:
        default_related_name = "dc_ac_efficiency_set"

class ChargingVoltage(HemsData):
    unit = "V"
    unit_verbose = "Voltage"

    class Meta:
        default_related_name = "charging_voltage_set"

class ChargingCurrent(HemsData):
    unit = "A"
    unit_verbose = "Amps"

    class Meta:
        default_related_name = "charging_current_set"

class ChargingRate(HemsData):
    unit = ""
    unit_verbose = ""

    class Meta:
        default_related_name = "charging_rate_set"

class ConverterEfficiency(HemsData):
    unit = "%%"
    unit_verbose = "Percent"

    class Meta:
        default_related_name = "converter_efficiency_set"

class DischargingVoltage(HemsData):
    unit = "V"
    unit_verbose = "Voltage"

    class Meta:
        default_related_name = "discharging_voltage_set"

class DischargingCurrent(HemsData):
    unit = "A"
    unit_verbose = "Amps"

    class Meta:
        default_related_name = "discharging_current_set"

class DischargingRate(HemsData):
    unit = ""
    unit_verbose = ""

    class Meta:
        default_related_name = "discharging_rate_set"

class StateOfCharge(HemsData):
    unit = "%%"
    unit_verbose = "Percent"

    class Meta:
        default_related_name = "state_of_charge_set"



######################## IN and OUT #######################
class SolarPVIn(models.Model):
    solarPV = models.OneToOneField(SolarPV, on_delete=models.CASCADE, related_name='in_set', null=True)
    incidentRadiations = GenericRelation(IncidentRadiation)

class SolarPVOut(models.Model):
    solarPV = models.OneToOneField(SolarPV, on_delete=models.CASCADE, related_name='out_set', null=True)
    dc_powers = GenericRelation(DCPower)
    energies = GenericRelation(Energy)
    voltages = GenericRelation(Voltage)
    currents = GenericRelation(Current)

class InverterIn(models.Model):
    inverter = models.OneToOneField(Inverter, on_delete=models.CASCADE, related_name='in_set')
    dc_powers = GenericRelation(DCPower)
    energies = GenericRelation(Energy)
    voltages = GenericRelation(Voltage)
    currents = GenericRelation(Current)

class InverterOut(models.Model):
    inverter = models.OneToOneField(Inverter, on_delete=models.CASCADE, related_name='out_set')
    ac_powers = GenericRelation(ACPower)
    energies = GenericRelation(Energy)
    voltages = GenericRelation(Voltage)
    currents = GenericRelation(Current)

class GridIn(models.Model):
    grid = models.OneToOneField(Grid, on_delete=models.CASCADE, related_name='in_set')
    ac_powers = GenericRelation(ACPower)
    energies = GenericRelation(Energy)
    voltages = GenericRelation(Voltage)
    currents = GenericRelation(Current)

class GridOut(models.Model):
    grid = models.OneToOneField(Grid, on_delete=models.CASCADE, related_name='out_set')
    ac_powers = GenericRelation(ACPower)
    energies = GenericRelation(Energy)
    voltages = GenericRelation(Voltage)
    currents = GenericRelation(Current)

class LoadIn(models.Model):
    load = models.OneToOneField(Load, on_delete=models.CASCADE, related_name='in_set')
    ac_powers = GenericRelation(ACPower)
    energies = GenericRelation(Energy)
    voltages = GenericRelation(Voltage)
    currents = GenericRelation(Current)

class BatteryIn(models.Model):
    battery = models.OneToOneField(Battery, on_delete=models.CASCADE, related_name='in_set')
    ac_powers = GenericRelation(ACPower)
    energies = GenericRelation(Energy)
    charging_voltage = GenericRelation(ChargingVoltage)
    charging_current = GenericRelation(ChargingCurrent)
    charging_rate = GenericRelation(ChargingRate)
    converter_efficiency = GenericRelation(ConverterEfficiency)

class BatteryOut(models.Model):
    battery = models.OneToOneField(Battery, on_delete=models.CASCADE, related_name='out_set')
    dc_powers = GenericRelation(DCPower)
    energies = GenericRelation(Energy)
    discharging_voltage = GenericRelation(DischargingVoltage)
    discharging_current = GenericRelation(DischargingCurrent)
    discharging_rate = GenericRelation(DischargingRate)
    converter_efficiency = GenericRelation(ConverterEfficiency)
    state_of_charge = GenericRelation(StateOfCharge)
