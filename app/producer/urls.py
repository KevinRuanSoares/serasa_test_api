"""
URL mappings for the user API.
"""
from django.urls import path

from producer import views


app_name = 'producer'

urlpatterns = [
    path('', views.ProducerManagementView.as_view(), name='list_create_producer'),
    path('<uuid:id>/', views.ProducerRetrieveUpdateView.as_view(), name='update_retrieve_producer'),
    path('farm/', views.FarmManagementView.as_view(), name='list_create_farm'),
    path('farm/<uuid:id>/', views.FarmRetrieveUpdateView.as_view(), name='update_retrieve_farm'),
]
