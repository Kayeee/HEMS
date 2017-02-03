from django.shortcuts import render, redirect
from . import forms

def index(request):
    form = forms.NameForm()
    return render(request, 'HEMSapp/index.html', {'form': form})

def ratePayerDash(request):
    name = request.user.profile
    print name
    return render(request, 'HEMSapp/ratePayerDash.html', {'name': name})
