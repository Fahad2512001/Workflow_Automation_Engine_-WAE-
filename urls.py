from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from core import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('core.urls')),
    path('user/', views.user_profile, name='user_profile'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    

    # Redirect root URL to dashboard
    path('', lambda request: redirect('dashboard/')),
    path('', include('core.urls')),
]

