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
    path('crops/', views.CropManagementView.as_view(), name='list_create_crop'),
    path('crops/<uuid:id>/', views.CropRetrieveUpdateView.as_view(), name='update_retrieve_crop'),
    path('harvests/', views.HarvestManagementView.as_view(), name='list_create_harvest'),
    path('harvests/<uuid:id>/', views.HarvestRetrieveUpdateView.as_view(), name='update_retrieve_harvest'),
    path('planted-crops/', views.PlantedCropManagementView.as_view(), name='list_create_planted_crop'),
    path(
        'planted-crops/<uuid:id>/',
        views.PlantedCropRetrieveUpdateView.as_view(),
        name='update_retrieve_planted_crop'
    ),
]
