from rest_framework import serializers
from django.contrib.auth import get_user_model
from generic_relations.relations import GenericRelatedField
from itertools import chain

from HEMSapp.models import *
################### HEMS REVISION ###################
class HemsUserSerializer(serializers.ModelSerializer):
    hemsbox_set = serializers.PrimaryKeyRelatedField(many=False, required=False, queryset=HemsBox.objects.all())

    class Meta:
        model = HemsUser
        fields = ('id', 'email', 'is_active', 'is_admin', 'first_name',
                'last_name', 'hemsbox_set', 'password')

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password'],
        )

        return user

class HemsBoxSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    solarPV_set = serializers.PrimaryKeyRelatedField(many=True, queryset=SolarPV.objects.all())
    inverter_set = serializers.PrimaryKeyRelatedField(many=True, queryset=Inverter.objects.all())
    grid_set = serializers.PrimaryKeyRelatedField(many=True, queryset=Grid.objects.all())
    load_set = serializers.PrimaryKeyRelatedField(many=True, queryset=Load.objects.all())
    battery_set = serializers.PrimaryKeyRelatedField(many=True, queryset=Battery.objects.all())

    class Meta:
        model = HemsBox
        fields = ('id', 'hemsID', 'owner', 'solarPV_set', 'inverter_set', 'grid_set', 'load_set', 'battery_set')


class SolarPVSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = SolarPV
        fields = ('id', 'name', 'owner', 'hems_box', 'status', 'manufacturer')


class SolarPVInSerializer(serializers.ModelSerializer):
    #incidentRadiations = serializers.PrimaryKeyRelatedField(many=True, queryset=IncidentRadiation.objects.all())
    unique_id = serializers.ReadOnlyField()

    class Meta:
        model = SolarPVIn
        fields = ('unique_id', 'solarPV')



class SolarPVOutSerializer(serializers.ModelSerializer):
    unique_id = serializers.ReadOnlyField()

    class Meta:
        model = SolarPVOut
        fields = ('unique_id', 'solarPV')

class InverterInSerializer(serializers.ModelSerializer):
    unique_id = serializers.ReadOnlyField()

    class Meta:
        model = InverterIn
        fields = ('unique_id', 'inverter')

class InverterOutSerializer(serializers.ModelSerializer):
    unique_id = serializers.ReadOnlyField()

    class Meta:
        model = InverterOut
        fields = ('unique_id', 'inverter')

class GridInSerializer(serializers.ModelSerializer):
    unique_id = serializers.ReadOnlyField()

    class Meta:
        model = GridIn
        fields = ('unique_id', 'grid')

class GridOutSerializer(serializers.ModelSerializer):
    unique_id = serializers.ReadOnlyField()

    class meta:
        model = GridOut
        fields = ('unique_id', 'grid')

class LoadInSerializer(serializers.ModelSerializer):
    unique_id = serializers.ReadOnlyField()

    class Meta:
        model = LoadIn
        fields = ('unique_id', 'load')

class BatteryInSerializer(serializers.ModelSerializer):
    unique_id = serializers.ReadOnlyField()

    class Meta:
        model = BatteryIn
        fields = ('unique_id', 'battery')

class BatteryOutSerializer(serializers.ModelSerializer):
    unique_id = serializers.ReadOnlyField()

    class meta:
        model = BatteryOut
        fields = ('unique_id', 'Battery')


############ Hems Data Serializers ###############
# class IncidentRadiationSerializer(serializers.ModelSerializer):
#     #The queryset parameter doesn't really matter since it will likely be changed
#     #in the IncidentRadiationDetail's "perform_create" method (see apiViews.py)
#     content_object = serializers.PrimaryKeyRelatedField(many=False, queryset=SolarPVIn.objects.all())
#
#     class Meta:
#         model = IncidentRadiation
#         fields = ('value', 'content_object')
# 
# class DCPowerSerializer(serializers.ModelSerializer):
#
#     content_object = serializers.PrimaryKeyRelatedField(many=False, queryset=SolarPVOut.objects.all())
#
#     class Meta:
#         model = DCPower
#         fields = ('value', 'content_object')
#
# class EnergySerializer(serializers.ModelSerializer):
#
#     content_object = serializers.PrimaryKeyRelatedField(many=False, queryset=SolarPVOut.objects.all())
#
#     class Meta:
#         model = Energy
#         fields = ('value', 'content_object')
#
# class VoltageEnergySerializer(serializers.ModelSerializer):
#
#     content_object = serializers.PrimaryKeyRelatedField(many=False, queryset=SolarPVOut.objects.all())
#
#     class Meta:
#         model = Voltage
#         fields = ('value', 'content_object')
#
# class CurrentSerializer(serializers.ModelSerializer):
#
#     content_object = serializers.PrimaryKeyRelatedField(many=False, queryset=SolarPVOut.objects.all())
#
#     class Meta:
#         model = Current
#         fields = ('value', 'content_object')
#
# class ACPowerSerializer(serializers.ModelSerializer):
#
#     content_object = serializers.PrimaryKeyRelatedField(many=False, queryset=SolarPVOut.objects.all())
#
#     class Meta:
#         model = ACPower
#         fields = ('value', 'content_object')
#
# class ReactivePowerSerializer(serializers.ModelSerializer):
#
#     content_object = serializers.PrimaryKeyRelatedField(many=False, queryset=SolarPVOut.objects.all())
#
#     class Meta:
#         model = ReactivePower
#         fields = ('value', 'content_object')
#
# class DCACEfficiencySerializer(serializers.ModelSerializer):
#
#     content_object = serializers.PrimaryKeyRelatedField(many=False, queryset=SolarPVOut.objects.all())
#
#     class Meta:
#         model = DCACEfficiency
#         fields = ('value', 'content_object')
#
# class ChargingVoltageSerializer(serializers.ModelSerializer):
#
#     content_object = serializers.PrimaryKeyRelatedField(many=False, queryset=SolarPVOut.objects.all())
#
#     class Meta:
#         model = ChargingVoltage
#         fields = ('value', 'content_object')
#
# class ChargingCurrentSerializer(serializers.ModelSerializer):
#
#     content_object = serializers.PrimaryKeyRelatedField(many=False, queryset=SolarPVOut.objects.all())
#
#     class Meta:
#         model = ChargingCurrent
#         fields = ('value', 'content_object')
#
# class ChargingRateSerializer(serializers.ModelSerializer):
#
#     content_object = serializers.PrimaryKeyRelatedField(many=False, queryset=SolarPVOut.objects.all())
#
#     class Meta:
#         model = ChargingRate
#         fields = ('value', 'content_object')
#
# class ConverterEfficiencySerializer(serializers.ModelSerializer):
#
#     content_object = serializers.PrimaryKeyRelatedField(many=False, queryset=SolarPVOut.objects.all())
#
#     class Meta:
#         model = ConverterEfficiency
#         fields = ('value', 'content_object')
#
# class DischargingVoltageSerializer(serializers.ModelSerializer):
#
#     content_object = serializers.PrimaryKeyRelatedField(many=False, queryset=SolarPVOut.objects.all())
#
#     class Meta:
#         model = DischargingVoltage
#         fields = ('value', 'content_object')
#
# class DischargingCurrentSerializer(serializers.ModelSerializer):
#
#     content_object = serializers.PrimaryKeyRelatedField(many=False, queryset=SolarPVOut.objects.all())
#
#     class Meta:
#         model = DischargingCurrent
#         fields = ('value', 'content_object')
#
# class DischargingRateSerializer(serializers.ModelSerializer):
#
#     content_object = serializers.PrimaryKeyRelatedField(many=False, queryset=SolarPVOut.objects.all())
#
#     class Meta:
#         model = DischargingRate
#         fields = ('value', 'content_object')
#
# class StateOfChargeSerializer(serializers.ModelSerializer):
#
#     content_object = serializers.PrimaryKeyRelatedField(many=False, queryset=SolarPVOut.objects.all())
#
#     class Meta:
#         model = StateOfCharge
#         fields = ('value', 'content_object')

##############Generic Serializer#############
class HemsDataSerializer(serializers.Serializer):

    #content_object = serializers.PrimaryKeyRelatedField(many=False, queryset=SolarPVIn.objects.all())
    value = serializers.FloatField()

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        print type(validated_data['content_object'])
        print validated_data
        return obj.objects.create(**validated_data)
