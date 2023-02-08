from django.contrib.auth import views as views_auth
from . import views
from django.urls import path, reverse_lazy

app_name = 'users'


urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('logout/',
         views_auth.LogoutView.as_view(template_name='users/logged_out.html'),
         name='logout'),
    path('login/',
         views_auth.LoginView.as_view(template_name='users/login.html'),
         name='login'),
    path('password_change/',
         views_auth.PasswordChangeView.as_view(
             success_url=reverse_lazy('users:password_change_done'),
             template_name='users/password_change_form.html'),
         name='password_change'),
    path('password_change/done/',
         views_auth.PasswordChangeDoneView.as_view(
             template_name='users/password_change_done.html'),
         name='password_change_done'),
    path('password_reset/',
         views_auth.PasswordResetView.as_view(
             success_url=reverse_lazy('users:password_reset_done'),
             template_name='users/password_reset_form.html',
             email_template_name='users/password_reset_email.html'),
         name='password_reset_form'),
    path('password_reset/done/',
         views_auth.PasswordResetDoneView.as_view(
             template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         views_auth.PasswordResetConfirmView.as_view(
             success_url=reverse_lazy('users:password_reset_complete'),
             template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         views_auth.PasswordResetCompleteView.as_view(
             template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
