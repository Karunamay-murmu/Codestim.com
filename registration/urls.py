from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from .views import User_signup, User_login, User_logout
from .forms import ResetPasswordForm

from compression_middleware.decorators import compress_page

app_name = 'registration'

urlpatterns = [
    path('signup/', compress_page(User_signup.as_view()), name='sign_up'),
    path('login/', compress_page(User_login.as_view()), name='log_in'),
    path('logout/', compress_page(User_logout), name='log_out'),
    path('password-reset/', compress_page(auth_views.PasswordResetView.as_view(template_name='authentication/resetPasswordFlow.html', success_url=reverse_lazy('registration:password_reset_done'))),
         name='password_reset'),

    path('password-reset/sent/', compress_page(auth_views.PasswordResetDoneView.as_view(template_name='authentication/resetPasswordFlow.html')),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', compress_page(auth_views.PasswordResetConfirmView.as_view(
        template_name='authentication/resetPasswordForm.html',
        success_url=reverse_lazy('registration:password_reset_complete'),
        form_class=ResetPasswordForm
    )), name='password_reset_confirm'),

    path('password-reset/success/', compress_page(auth_views.PasswordResetCompleteView.as_view(
         template_name='authentication/resetPasswordFlow.html'
         )), name='password_reset_complete')
]
