from django.urls import path
from . import views

urlpatterns = [
    # path(r'api/v1', views.overview, name='overview'),
    path(r'api/v1/<str:summoner>', views.predictorView, name='predictorView'),
]

