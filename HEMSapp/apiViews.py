from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.contrib import auth
from django.http import HttpResponse, Http404, HttpResponseRedirect
from rest_framework import generics
from rest_framework.views import APIView

from models import *
from serializers import *



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

    def perform_create(self, serializer):
        print serializer.data

class SolarPVInDetail(generics.RetrieveAPIView):
    queryset = SolarPVIn.objects.all()
    serializer_class = SolarPVInSerializer


class SolarPVOutList(generics.ListCreateAPIView):
    queryset = SolarPVOut.objects.all()
    serializer_class = SolarPVOutSerializer


class SolarPVOutDetail(generics.RetrieveAPIView):
    queryset = SolarPVOut.objects.all()
    serializer_class = SolarPVOutSerializer

#################### Assets ###################
class IncidentRadiationList(generics.ListCreateAPIView):
    queryset = IncidentRadiation.objects.all()
    serializer_class = IncidentRadiationSerializer

    def perform_create(self, serializer):
        print serializer.data

class IncidentRadiationDetail(generics.RetrieveAPIView):
    queryset = IncidentRadiation.objects.all()
    serializer_class = IncidentRadiationSerializer
