from django.urls import path

from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:activity_id>/', views.activity_page, name='app'),
    path('data/<int:activity_id>/', views.activity_data, name='activity_data')
]
