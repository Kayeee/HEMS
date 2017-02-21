from rest_framework import serializers
from django.contrib.auth import get_user_model
from generic_relations.relations import GenericRelatedField

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
    incidentRadiations = serializers.PrimaryKeyRelatedField(many=True, queryset=IncidentRadiation.objects.all())

    class Meta:
        model = SolarPVIn
        fields = ('id', 'solarPV', 'incidentRadiations')



class SolarPVOutSerializer(serializers.ModelSerializer):

    class Meta:
        model = SolarPVOut
        fields = ('id', 'solarPV')

class IncidentRadiationSerializer(serializers.ModelSerializer):
    # I NEED HELP HERE. HOW DO I SERIALIZE INCIDENT RADIATION WHEN IT IS GENERIC?


    # content_object = serializers.RelatedField(queryset=SolarPVIn.objects.all())
    content_object = serializers.HyperlinkedRelatedField(
            queryset = SolarPVIn.objects.all(),
            view_name='solarPV-detail',
            many=True
        ),

    class Meta:
        model = IncidentRadiation
        fields = ('value', 'content_object')
