from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import View
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


# class CustomLoginView(SuccessMessageMixin, LoginView):
#     form = CustomAuthenticationForm
#     template_name = 'users/login.html'
#     success_message = 'Success: You were successfully logged in.'
#     success_url = reverse_lazy('tours:base_view')


from django.contrib.auth import authenticate, login

class CustomLoginView(View):
    template_name = 'users/login.html'
    form = CustomAuthenticationForm
    message_send = 'Success: You were successfully logged in.'

    def get(self, request, *args, **kwargs):
        form = self.form
        context = {'form': form}
        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(email = email, password = password)
            if user:
                login(self.request, user)
                messages.success(self.request, self.message_send)
            return HttpResponseRedirect('/')
        context = {'form': form}
        return render(self.request, self.template_name, context)


# class CustomRegistrationView(View):
#     template_name = 'users/registration.html'
#     form = CustomUserCreationForm
#     message = 'Your account has been created! You are now able to log in.'
#
#     def get(self, request, *args, **kwargs):
#         context = {'form':self.form}
#         return render(self.request, self.template_name, context)
#
#     def post(self, request, *args,**kwargs):
#         form = self.form(request.POST or None)
#         if form.is_valid():
#             user = form.save()
#             user.set_password(user.password)
#             user.save()
#             messages.add_message(self.request, messages.SUCCESS, self.message)
#             return HttpResponseRedirect('/')
#
#         form = self.form(request.POST)
#         context = {'form':form}
#         return render(self.request, self.template_name, context)

from django.views.generic import CreateView

class CustomRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        form.instance.pass_test = form.cleaned_data['password1']
        return super(CustomRegistrationView, self).form_valid(form)