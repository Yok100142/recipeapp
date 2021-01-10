from django.urls import path

from . import error_views
app_name = 'error'
urlpatterns = [
    path('', error_views.index, name='index'),
    path('delete_report/<str:id>', error_views.delete_report, name='delete_report'),
    path('delete_data/<str:id>', error_views.delete_data, name='delete_data'),
    path('recipe_list/', error_views.DataList, name='DataList'),
    path('recipe_list/<str:id>', error_views.editDataList, name='editDataList'),
    path('edit_report/<str:reportid>/<str:id>', error_views.editReport, name='editReport'),
    path('update_report/<str:reportid>/<str:id>', error_views.update_report, name='update_report'),
    path('update_data/<str:id>', error_views.update_data, name='update_data'),
    
]


