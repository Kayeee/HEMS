from django.shortcuts import render, redirect

def index(request):
    return render(request, 'HEMSapp/index.html')

def ratePayerDash(request):
    return render(request, 'HEMSapp/ratePayerDash.html')
