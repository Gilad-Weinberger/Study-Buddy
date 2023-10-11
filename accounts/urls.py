from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('user/<int:user_id>/', views.user_details, name='user_details'),
    path('accounts/edit_details/<int:user_id>/', views.edit_details, name='edit_details'),
]
