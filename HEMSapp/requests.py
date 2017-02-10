from django.core.context_processors import csrf
from django.contrib import auth, messages
from django.http import HttpResponse, Http404, HttpResponseRedirect

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
