from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.contrib import auth
from django.http import HttpResponse, Http404, HttpResponseRedirect
from rest_framework import generics
from rest_framework.views import APIView

from models import *
from serializers import *

hems_data_types = {
    "IncidentRadiation": IncidentRadiation,
    "DCPower": DCPower,
    "Energy": Energy,
    "Voltage": Voltage,
    "Current": Current,
    "ACPower": ACPower,
    "ReactivePower": ReactivePower,
    "DCACEfficiency": DCACEfficiency,
    "ChargingVoltage": ChargingVoltage,
    "ChargingCurrent": ChargingCurrent,
    "ChargingRate": ChargingRate,
    "ConverterEfficiency": ConverterEfficiency,
    "DischargingVoltage": DischargingVoltage,
    "DischargingCurrent": DischargingCurrent,
    "DischargingRate": DischargingRate,
    "StateOfCharge": StateOfCharge,
}

def get_content_object(content_object):
    """
    get the appropriate queryset based on the Asset and Direction
    """
    asset_direction = content_object.rstrip('1234567890')
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
    return query_set.get(unique_id=content_object)


################### Class Views ##################
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

class InverterInList(generics.ListCreateAPIView):
    queryset = InverterIn.objects.all()
    serializer_class = InverterInSerializer


class InverterInDetail(generics.RetrieveAPIView):
    queryset = InverterIn.objects.all()
    serializer_class = InverterInSerializer

class InverterOutList(generics.ListCreateAPIView):
    queryset = InverterOut.objects.all()
    serializer_class = InverterOutSerializer


class InverterOutDetail(generics.RetrieveAPIView):
    queryset = InverterOut.objects.all()
    serializer_class = InverterOutSerializer

class GridInList(generics.ListCreateAPIView):
    queryset = GridIn.objects.all()
    serializer_class = GridInSerializer


class GridInDetail(generics.RetrieveAPIView):
    queryset = GridIn.objects.all()
    serializer_class = GridInSerializer


class GridOutList(generics.ListCreateAPIView):
    queryset = GridOut.objects.all()
    serializer_class = GridOutSerializer


class GridOutDetail(generics.RetrieveAPIView):
    queryset = GridOut.objects.all()
    serializer_class = GridOutSerializer

class LoadInList(generics.ListCreateAPIView):
    queryset = LoadIn.objects.all()
    serializer_class = LoadInSerializer


class LoadInDetail(generics.RetrieveAPIView):
    queryset = LoadIn.objects.all()
    serializer_class = LoadInSerializer

class BatteryInList(generics.ListCreateAPIView):
    queryset = BatteryIn.objects.all()
    serializer_class = BatteryInSerializer


class BatteryInDetail(generics.RetrieveAPIView):
    queryset = BatteryIn.objects.all()
    serializer_class = BatteryInSerializer

class BatteryOutList(generics.ListCreateAPIView):
    queryset = BatteryOut.objects.all()
    serializer_class = BatteryOutSerializer


class BatteryOutDetail(generics.RetrieveAPIView):
    queryset = BatteryOut.objects.all()
    serializer_class = BatteryOutSerializer
#################### HEMS data ###################


# class IncidentRadiationList(generics.ListCreateAPIView):
#     queryset = IncidentRadiation.objects.all()
#     serializer_class = IncidentRadiationSerializer
#
#     def perform_create(self, serializer):
#         self.queryset = get_data_queryset(self.request.data['data_type'])
#         content_object = get_content_object(self.request.data['content_object'])
#         print serializer.save(content_object=content_object)
#
# class IncidentRadiationDetail(generics.RetrieveDestroyAPIView):
#     queryset = IncidentRadiation.objects.all()
#     serializer_class = IncidentRadiationSerializer
#
# class DCPowerList(generics.ListCreateAPIView):
#     queryset = DCPower.objects.all()
#     serializer_class = DCPowerSerializer
#
#     def perform_create(self, serializer):
#         content_object = get_content_object(self.request.data['content_object'])
#         print serializer.save(content_object=content_object)
#
# class DCPowerDetail(generics.RetrieveAPIView):
#     queryset = DCPower.objects.all()
#     serializer_class = DCPowerSerializer
#
# class EnergyList(generics.ListCreateAPIView):
#     queryset = Energy.objects.all()
#     serializer_class = EnergySerializer
#
#     def perform_create(self, serializer):
#         content_object = get_content_object(self.request.data['content_object'])
#         print serializer.save(content_object=content_object)
#
# class EnergyDetail(generics.RetrieveAPIView):
#     queryset = Energy.objects.all()
#     serializer_class = EnergySerializer
#
#
# class VoltageList(generics.ListCreateAPIView):
#     queryset = Voltage.objects.all()
#     serializer_class = VoltageSerializer
#
#     def perform_create(self, serializer):
#         content_object = get_content_object(self.request.data['content_object'])
#         print serializer.save(content_object=content_object)
#
# class VoltageDetail(generics.RetrieveAPIView):
#     queryset = Voltage.objects.all()
#     serializer_class = VoltageSerializer
#
#
# class CurrentList(generics.ListCreateAPIView):
#     queryset = Current.objects.all()
#     serializer_class = CurrentSerializer
#
#     def perform_create(self, serializer):
#         content_object = get_content_object(self.request.data['content_object'])
#         print serializer.save(content_object=content_object)
#
# class CurrenteDetail(generics.RetrieveAPIView):
#     queryset = Current.objects.all()
#     serializer_class = CurrentSerializer
#
#
# class ACPowerList(generics.ListCreateAPIView):
#     queryset = ACPower.objects.all()
#     serializer_class = ACPowerSerializer
#
#     def perform_create(self, serializer):
#         content_object = get_content_object(self.request.data['content_object'])
#         print serializer.save(content_object=content_object)
#
# class ACPowerDetail(generics.RetrieveAPIView):
#     queryset = ACPower.objects.all()
#     serializer_class = ACPowerSerializer
#
#
# class ReactivePowerList(generics.ListCreateAPIView):
#     queryset = ReactivePower.objects.all()
#     serializer_class = ReactivePowerSerializer
#
#     def perform_create(self, serializer):
#         content_object = get_content_object(self.request.data['content_object'])
#         print serializer.save(content_object=content_object)
#
# class ReactivePowerDetail(generics.RetrieveAPIView):
#     queryset = ReactivePower.objects.all()
#     serializer_class = ReactivePowerSerializer
#
#
# class BCACEfficiencyList(generics.ListCreateAPIView):
#     queryset = BCACEfficiency.objects.all()
#     serializer_class = BCACEfficiencySerializer
#
#     def perform_create(self, serializer):
#         content_object = get_content_object(self.request.data['content_object'])
#         print serializer.save(content_object=content_object)
#
# class BCACEfficiencyDetail(generics.RetrieveAPIView):
#     queryset = BCACEfficiency.objects.all()
#     serializer_class = BCACEfficiencySerializer
#
#
# class ChargingVoltageList(generics.ListCreateAPIView):
#     queryset = ChargingVoltage.objects.all()
#     serializer_class = ChargingVoltageSerializer
#
#     def perform_create(self, serializer):
#         content_object = get_content_object(self.request.data['content_object'])
#         print serializer.save(content_object=content_object)
#
# class ChargingVoltageDetail(generics.RetrieveAPIView):
#     queryset = ChargingVoltage.objects.all()
#     serializer_class = ChargingVoltageSerializer
#
#
# class ChargingCurrentList(generics.ListCreateAPIView):
#     queryset = ChargingCurrent.objects.all()
#     serializer_class = ChargingCurrentSerializer
#
#     def perform_create(self, serializer):
#         content_object = get_content_object(self.request.data['content_object'])
#         print serializer.save(content_object=content_object)
#
# class ChargingCurrentDetail(generics.RetrieveAPIView):
#     queryset = ChargingCurrent.objects.all()
#     serializer_class = ChargingCurrentSerializer
#
#
# class ChargingRateList(generics.ListCreateAPIView):
#     queryset = ChargingRate.objects.all()
#     serializer_class = ChargingRateSerializer
#
#     def perform_create(self, serializer):
#         content_object = get_content_object(self.request.data['content_object'])
#         print serializer.save(content_object=content_object)
#
# class ChargingRateDetail(generics.RetrieveAPIView):
#     queryset = ChargingRate.objects.all()
#     serializer_class = ChargingRateSerializer
#
#
# class ConverterEfficiencyList(generics.ListCreateAPIView):
#     queryset = ConverterEfficiency.objects.all()
#     serializer_class = ConverterEfficiencySerializer
#
#     def perform_create(self, serializer):
#         content_object = get_content_object(self.request.data['content_object'])
#         print serializer.save(content_object=content_object)
#
# class ConverterEfficiencyDetail(generics.RetrieveAPIView):
#     queryset = ConverterEfficiency.objects.all()
#     serializer_class = ConverterEfficiencySerializer
#
#
# class DischargingVoltageList(generics.ListCreateAPIView):
#     queryset = DischargingVoltage.objects.all()
#     serializer_class = DischargingVoltageSerializer
#
#     def perform_create(self, serializer):
#         content_object = get_content_object(self.request.data['content_object'])
#         print serializer.save(content_object=content_object)
#
# class DischargingVoltageDetail(generics.RetrieveAPIView):
#     queryset = DischargingVoltage.objects.all()
#     serializer_class = DischargingVoltageSerializer
#
#
# class DischargingCurrentList(generics.ListCreateAPIView):
#     queryset = DischargingCurrent.objects.all()
#     serializer_class = DischargingCurrentSerializer
#
#     def perform_create(self, serializer):
#         content_object = get_content_object(self.request.data['content_object'])
#         print serializer.save(content_object=content_object)
#
# class DischargingCurrentDetail(generics.RetrieveAPIView):
#     queryset = DischargingCurrent.objects.all()
#     serializer_class = DischargingCurrentSerializer
#
#
# class DischargingRateList(generics.ListCreateAPIView):
#     queryset = DischargingRate.objects.all()
#     serializer_class = DischargingRateSerializer
#
#     def perform_create(self, serializer):
#         content_object = get_content_object(self.request.data['content_object'])
#         print serializer.save(content_object=content_object)
#
# class DischargingRateDetail(generics.RetrieveAPIView):
#     queryset = DischargingRate.objects.all()
#     serializer_class = DischargingRateSerializer
#
#
# class StateOfChargeList(generics.ListCreateAPIView):
#     queryset = StateOfCharge.objects.all()
#     serializer_class = StateOfChargeSerializer
#
#     def perform_create(self, serializer):
#         content_object = get_content_object(self.request.data['content_object'])
#         print serializer.save(content_object=content_object)
#
# class StateOfChargeDetail(generics.RetrieveAPIView):
#     queryset = StateOfCharge.objects.all()
#     serializer_class = StateOfChargeSerializer
#

import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def hemsDataCreate(request):
    data = json.loads(request.body)
    data_type = hems_data_types[data['data_type']]
    content_object = get_content_object(data['content_object'])

    try:
        data_type.objects.create(content_object=content_object, value=data['value'])
        return HttpResponse(status='201')
    except:
        return HttpResponse(status='500')
