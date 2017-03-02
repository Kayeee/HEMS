from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.contrib import auth
from django.http import HttpResponse, Http404, HttpResponseRedirect
from rest_framework import generics
from rest_framework.views import APIView

from models import *
from serializers import *


def get_content_queryset(asset_direction):
    """
    get the appropriate queryset based on the Asset and Direction
    """
    asset_directions = {
        "SolarPVIn": SolarPVIn,
        "SolarPVOut": SolarPVOut,
        "InverterIn": InverterIn,
        "InverterOut": InverterOut,
        "GridIn": GridIn,
        "GridOut": GridOut,
        "LoadIn": LoadIn,
        "BatteryIn": BatteryIn,
        "BatteryOut": BatteryOut
    }

    query_set = asset_directions[asset_direction].objects.all()
    return query_set

class UserList(generics.ListCreateAPIView):
    queryset = HemsUser.objects.all()
    serializer_class = HemsUserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = HemsUser.objects.all()
    serializer_class = HemsUserSerializer


class HemsBoxList(generics.ListCreateAPIView):
    queryset = HemsBox.objects.all()
    serializer_class = HemsBoxSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class HemsBoxDetail(generics.RetrieveAPIView):
    queryset = HemsBox.objects.all()
    serializer_class = HemsBoxSerializer

################## Assets ##################
class SolarPVList(generics.ListCreateAPIView):
    queryset = SolarPV.objects.all()
    serializer_class = SolarPVSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class SolarPVDetail(generics.RetrieveAPIView):
    queryset = SolarPV.objects.all()
    serializer_class = SolarPVSerializer


##################### In and Out #################
class SolarPVInList(generics.ListCreateAPIView):
    queryset = SolarPVIn.objects.all()
    serializer_class = SolarPVInSerializer

class SolarPVInDetail(generics.RetrieveDestroyAPIView):
    queryset = SolarPVIn.objects.all()
    serializer_class = SolarPVInSerializer


class SolarPVOutList(generics.ListCreateAPIView):
    queryset = SolarPVOut.objects.all()
    serializer_class = SolarPVOutSerializer


class SolarPVOutDetail(generics.RetrieveAPIView):
    queryset = SolarPVOut.objects.all()
    serializer_class = SolarPVOutSerializer

#################### HEMS data ###################
class IncidentRadiationList(generics.ListCreateAPIView):
    queryset = IncidentRadiation.objects.all()
    serializer_class = IncidentRadiationSerializer

    def perform_create(self, serializer):
        print self.request.data['content_object']

        #content_obj = self.request.data['content_object']
        content_query_set = get_content_queryset(self.request.data['asset_direction_type'])
        obj = content_query_set.get(unique_id=self.request.data['content_object'])

        print serializer.save(content_object=obj)

class IncidentRadiationDetail(generics.RetrieveDestroyAPIView):
    queryset = IncidentRadiation.objects.all()
    serializer_class = IncidentRadiationSerializer

class DCPowerList(generics.ListCreateAPIView):
    queryset = DCPower.objects.all()
    serializer_class = DCPowerSerializer

    def perform_create(self, serializer):
        content_query_set = get_content_queryset(self.request.data['asset_direction_type'])
        obj = content_query_set.get(unique_id=self.request.data['content_object'])

        serializer.save(content_object=obj)

class DCPowerDetail(generics.RetrieveAPIView):
    queryset = DCPower.objects.all()
    serializer_class = DCPowerSerializer
