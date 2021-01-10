from django.urls import path

from . import dict_views
app_name = 'dict'
urlpatterns = [
    path('', dict_views.index, name='index'),
    path('errorlist', dict_views.errorlist, name='errorlist'),
    
]


