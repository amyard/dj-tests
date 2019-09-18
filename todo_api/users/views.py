from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View, CreateView
from django.contrib import messages
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

from .forms import CustomAuthenticationForm, CustomUserCreationForm

class CustomLogoutView(LogoutView):
    def get_next_page(self):
        next_page = super(CustomLogoutView, self).get_next_page()
        messages.add_message(self.request, messages.SUCCESS, 'Success: You successfully log out!')
        return next_page


class CustomLoginView(SuccessMessageMixin, LoginView):
    form = CustomAuthenticationForm
    template_name = 'users/login.html'
    success_message = 'Success: You were successfully logged in.'
    success_url = reverse_lazy('tours:base_view')


class CustomRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('tasks:base_view')

    def form_valid(self, form):
        form.instance.pass_test = form.cleaned_data['password1']
        return super(CustomRegistrationView, self).form_valid(form)


