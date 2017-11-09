from django.shortcuts import render, redirect
from . import forms
from models import GridOut, GridPowerNet, get_assets

def index(request):
    form = forms.NameForm()
    return render(request, 'HEMSapp/index.html', {'form': form})

def home(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    context = {
        'first_name': first_name,
        'last_name': last_name,
    } 
    grid_out = GridOut.objects.filter(grid__owner=request.user)
    if len(grid_out) > 0:    
        grid_out = grid_out[0]
	first_data = GridPowerNet.objects.filter(object_id=grid_out.unique_id,).first()
    	first_month = first_data.timestamp.strftime('%B %Y') # so we know where to start our chart
        context['first_month'] = first_month
    boxes = get_assets(request.user.hemsbox_set.all()) #func comes from models.py
 
    context['boxes'] = boxes
   

    return render(request, 'HEMSapp/ratePayerDash.html', context)

def registerDevice(request):
    return render(request, 'HEMSapp/registerDevice.html')

def addAsset(request):
    return render(request, 'HEMSapp/addAsset.html')
