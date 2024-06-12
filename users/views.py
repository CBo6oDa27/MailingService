import secrets

from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import PasswordRecoveryForm, UserProfileForm, UserRegisterForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Перейдите по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse_lazy("users:login"))


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user


class CustomLoginView(LoginView):
    template_name = "users/login.html"

    def get_success_url(self):
        return super().get_success_url()


class PasswordRecoveryView(TemplateView):
    model = User
    template_name = "users/password_recovery_form.html"
    form_class = PasswordRecoveryForm
    success_url = reverse_lazy("users:login")

    code = secrets.token_hex(8)

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        user = User.objects.get(email=email)
        code = self.code
        user.set_password(code)
        user.save()

        send_mail(
            "Восстановление пароля",
            f"Ваш новый пароль {code}",
            EMAIL_HOST_USER,
            [user.email],
        )
        return redirect(reverse_lazy("users:login"))
