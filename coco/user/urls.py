from django.urls import path
from .views import *

app_name = 'user'
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('new_profile/', new_profile, name='new_profile'),
    path('create_profile/', create_profile, name='create_profile'),
]