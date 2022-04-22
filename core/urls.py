from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_docs, name='upload_docs'),
]