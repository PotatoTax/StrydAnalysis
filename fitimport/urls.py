from django.urls import path

from . import views

app_name = 'fitparser'

urlpatterns = [
    path('', views.upload_fit, name='upload'),
]
