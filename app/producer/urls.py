"""
URL mappings for the user API.
"""
from django.urls import path

from producer import views


app_name = 'producer'

urlpatterns = [
    path('', views.ProducerManagementView.as_view(), name='list_create'),
    path('<uuid:id>/', views.ProducerRetrieveUpdateView.as_view(), name='update_retrieve'),
]
