from rest_framework import serializers
from HEMSapp.models import *

# class ProjectSerializer(serializers.ModelSerializer):
#     owner = serializers.ReadOnlyField(source='owner.username')
#     upload = serializers.PrimaryKeyRelatedField(many=True, queryset=File.objects.all())
#
#     class Meta:
#         model = Project
#         fields = ('id', 'title', 'owner', 'upload')
#
#
# class FileSerializer(serializers.ModelSerializer):
#     project = serializers.ReadOnlyField(source='project.id')
#
#     class Meta:
#         model = File
#         fields = ('id', 'title', 'upload', 'project')
#
# class UserSerializer(serializers.ModelSerializer):
#     project = serializers.PrimaryKeyRelatedField(many=True, queryset=Project.objects.all())
#
#     class Meta:
#         model = MDBUser
#         fields = ('id', 'username', 'email', 'date_of_birth', 'is_active',
#                     'is_admin', 'first_name', 'last_name', 'project')
#

################### HEMS REVISION ###################
class HemsUserSerializer(serializers.ModelSerializer):
    hemsbox_set = serializers.PrimaryKeyRelatedField(many=False, required=False, queryset=HemsBox.objects.all())

    class Meta:
        model = HemsUser
        fields = ('id', 'email', 'is_active', 'is_admin', 'first_name', 'last_name', 'hemsbox_set')

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
    in_set = serializers.PrimaryKeyRelatedField(many=False, queryset=SolarPVIn.objects.all())
    out_set = serializers.PrimaryKeyRelatedField(many=False, queryset=SolarPVOut.objects.all())

    class Meta:
        model = SolarPV
        fields = ('id', 'name', 'status', 'manufacturer', 'created_date', 'in_set', 'out_set')


class SolarPVInSerializer(serializers.ModelSerializer):
    incidentRadiations = serializers.PrimaryKeyRelatedField(many=True, queryset=IncidentRadiation.objects.all())

    class Meta:
        model = SolarPVIn
        fields = ('id', 'solarPV', 'incidentRadiations')

class SolarPVOutSerializer(serializers.ModelSerializer):
    dc_powers = serializers.ReadOnlyField()
    energies = serializers.ReadOnlyField()
    voltages = serializers.ReadOnlyField()
    currents = serializers.ReadOnlyField()

    class Meta:
        model = SolarPVOut
        fields = ('id', 'solarPV', 'dc_powers', 'energies', 'voltages', 'currents')
