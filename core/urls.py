from django.urls import path
from core import views

urlpatterns = [
    path('', views.upload_docs, name='upload_docs'),
    path('compare_multiple/', views.compare_multiple, name='compare_multiple'),
    path('get_report/', views.generate_report, name='get_report'),
]