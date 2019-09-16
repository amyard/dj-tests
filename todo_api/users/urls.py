from django.urls import path, reverse_lazy
from .views import CustomLoginView, CustomLogoutView, CustomRegistrationView

app_name = 'users'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(next_page = reverse_lazy('tasks:base_view')), name='logout'),
    path('registration/', CustomRegistrationView.as_view(), name='registration'),
]