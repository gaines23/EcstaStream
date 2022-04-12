"""
Definition of urls for DjangoWebProject1.
"""
from datetime import datetime
from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from app.views import *
from app.forms import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls'), name="home"),
    path('login/', NewLoginView.as_view(redirect_authenticated_user=True, 
                                        template_name='users/login.html',
                                        authentication_form=LoginForm),
                                        name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
    path('password-change/', ChangePasswordView.as_view(), name='password-change'),
#   url(r'^oauth/', include('social_django.urls', namespace='social')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)