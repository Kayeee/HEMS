from django.shortcuts import render, redirect
from . import forms

def index(request):
    form = forms.NameForm()
    return render(request, 'HEMSapp/index.html', {'form': form})

def home(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    return render(request, 'HEMSapp/ratePayerDash.html', {'first_name': first_name, 'last_name': last_name})
