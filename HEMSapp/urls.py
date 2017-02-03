from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from . import views, requests

app_name = 'HEMSapp'
urlpatterns = [

    #views
    url(r'^$', views.index, name='index'),
    url(r'^ratePayerDash$', views.ratePayerDash, name='ratePayerDash'),


    #API views
    url(r'^login$', requests.login, name='login'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
    
]
