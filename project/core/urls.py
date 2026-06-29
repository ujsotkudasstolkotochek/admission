from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('api/programs-stats/', views.programs_stats_api, name='api_stats'),
]