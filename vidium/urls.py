from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'vidium'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('upload/', views.Upload.upload, name='upload'),
    path('sort/<key>/<order>/', views.Index.sort, name='sort'),
]