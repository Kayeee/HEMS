from django.core.context_processors import csrf
from django.contrib import auth, messages
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse

from models import *
import tasks

def login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username = username, password = password)

    if user:
        auth.login(request, user)
        return HttpResponseRedirect('home')

    else:

        request.path ='/'
        messages.add_message(request, messages.INFO, 'Invalid Login')
        return HttpResponseRedirect(request.path)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('login')

def registerDevice_api(request):
    print request.POST
    user = request.user
    hemsID = request.POST['hemsID']

    HemsBox.objects.create(owner=user, hemsID=hemsID)


def get_inverter_data(request, inverter_id):

    result = tasks.getAll.apply_async(args=[inverter_id], queue='outback', routing_key='outback')

    tries = 0
    while result.state != 'SUCCESS':
        print result.state
        tries += 1
        time.sleep(1)
        if tries > 4:
            break

    if tries > 4:
        result_json = '{}'
    else:
        result_json = result.get()

    print("result: {0}").format(result_json)
    return JsonResponse(result_json)
