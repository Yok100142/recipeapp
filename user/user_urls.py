from django.urls import path

from . import user_views
app_name = 'user'
urlpatterns = [
    path('login', user_views.login, name='login'),
    path('profile/', user_views.profile, name='profile'),
    path('profile/changepassword/', user_views.changepassword, name='changepassword'),
    path('signout', user_views.signout, name='signout'),
    path('', user_views.list, name='list'),
    path('create/', user_views.create, name='create'),
    path('delete/<int:id>/', user_views.delete, name='delete'),
    path('save/', user_views.save, name='save'),
    path('edit/<int:id>/', user_views.edit, name='edit'),
    path('update/<int:id>/', user_views.update, name='update'),
]


