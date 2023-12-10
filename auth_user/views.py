from typing import Any
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .forms import SignUpForm
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, TemplateView, View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.
class SignUpView(SuccessMessageMixin, CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'auth/signup.html'
    success_url = reverse_lazy('login')

    def send_verify_email(self, user):
        token = default_token_generator.make_token(user)
        verify_url = self.request.build_absolute_uri(f'/verify/{user.pk}/{token}')
        message = f'Здравствуйте, {user.username}! Перейдите по ссылке нижу для подтверждения почты:\n\n {verify_url}'
        send_mail('Подтверждение почты', message, 'jafarastana01@gmail.com', [user.email])

    def form_valid(self,form):
        response = super().form_valid(form)
        user = self.object
        user.is_active = False
        user.save()
        self.send_verify_email(user)
        return response

class Login(LoginView):
    template_name = 'auth/login.html'
    next_page = reverse_lazy('todo:main')

    def form_valid(self, form):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, form.get_user())
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(reverse_lazy('login')+'?active=false')

class UserLogoutView(LogoutView):
    next_page = 'login'

class VerifycationSuccess(TemplateView):
    template_name = 'email/verification_success.html'
    
    def get(self, request):
        return redirect('login')

class VerifycationError(TemplateView):
    template_name = 'email/verification_error.html'

class VerifyEmailView(View):
    def get(self, request, user_id, token):
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('verify_success')
        else:
            return redirect('verify_error')