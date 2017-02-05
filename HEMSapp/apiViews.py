from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.contrib import auth
from django.http import HttpResponse, Http404, HttpResponseRedirect
from rest_framework import generics
from rest_framework.views import APIView

from models import *
from serializers import *
