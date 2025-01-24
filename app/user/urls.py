"""
URL mappings for the user API.
"""
from django.urls import path

from user import views


app_name = 'user'

urlpatterns = [
    path('', views.UserManagementView.as_view(), name='list_create'),
    path('<uuid:id>/', views.UserRetrieveUpdateView.as_view(), name='update_retrieve'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('login_refresh/', views.RefreshTokenView.as_view(), name='login_refresh'),
    path('profile/', views.ProfileUserView.as_view(), name='profile'),
    path('password_recover_code/', views.RecoverPasswordCodeUserView.as_view(), name='recover_password_code'),
    path('password_validate_code/', views.ValidatePasswordCodeView.as_view(), name='validate_password_code'),
    path('password_change_code/', views.ChangePasswordCodeView.as_view(), name='change_password_code'),
]
