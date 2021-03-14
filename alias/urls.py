from django.urls import path
from .views import create_alias, get_target_by_alias

urlpatterns = [
    path('create_alias/', create_alias, name='create_alias'),
    path('get_object/', get_target_by_alias, name='get_target'),
]
