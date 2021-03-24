from django.urls import path
app_name = 'dashboard'
from . import dashboard_views
urlpatterns = [
    
    path('', dashboard_views.index, name='index'),
    path('search', dashboard_views.searchmain, name='searchmain'),
    path('search/<str:id>', dashboard_views.pagedata, name='pagedata'),
    path('sendreport/<str:id>', dashboard_views.sendreport, name='sendreport'),
    path('downloadIngrediwnDict', dashboard_views.downloadIngrediwnDict, name='downloadIngrediwnDict')
]