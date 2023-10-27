from django.shortcuts import render
from django.views.generic.edit import FormView
from django.views.generic import View, UpdateView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from datetime import datetime, timedelta


from .forms import UserRegisterForm, LoginForm, UpdatePasswordForm
from .models import User


# Create your views here.


class UserRegisterView(FormView):
    template_name = 'usuarios/register.html'
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):
        User.objects.create_superuser(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
        )
        return super(UserRegisterView, self).form_valid(form)
    

class LoginUser(FormView):
    template_name = 'usuarios/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('home_app:home_panel')

    def form_valid(self, form):
        user = authenticate(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password']
        )
        login(self.request, user)
        return super(LoginUser, self).form_valid(form)
    

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(
            reverse('usuarios_app:user-login')
        )
    
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "usuarios/update_user.html"
    form_class = UserRegisterForm
    success_url  = reverse_lazy('usuarios_app:update_user')
    login_url = reverse_lazy('usuarios_app:user-login')
    

class UpdatePassword(FormView):
    template_name = 'usuarios/update_user.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('usuarios_app:user-login')


    def form_valid(self, form):
        usuario = self.request.user
        user = authenticate(
            username = usuario.username,
            password = form.cleaned_data['password1']
        )
        if user:
            new_password = form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()
            logout(self.request)
            return super(UpdatePassword, self).form_valid(form)
        else:
            form.add_error(None, 'Incorrect old password')
            messages.error(self.request, 'Incorrect old password. Please try again.')
            return self.form_invalid(form)
            
