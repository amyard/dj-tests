from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


from .models import Project
from .forms import ProjectCreateForm, ProjectUpdateForm


def index(request):
    user = request.user
    return render(request, 'base.html', context = {'test':'LALALLALALAA', 'user':user})


class ProjectListView(ListView):
    model = Project
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


class ProjectCreateView(LoginRequiredMixin, CreateView):
    template_name = 'tasks/project_create.html'
    form_class = ProjectCreateForm

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ProjectCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ProjectCreateView, self).form_valid(form)

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Success: Project was created.')
        return reverse('tasks:project_list')


class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectUpdateForm
    template_name = 'tasks/project_create.html'

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ProjectUpdateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        kwargs['slug'] = self.kwargs['slug']
        return kwargs

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Success: Project was updated.')
        return reverse('tasks:project_list')

    def test_func(self):
        pr = self.get_object()
        if self.request.user == pr.user or self.request.user.is_superuser:
            return True
        return False


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Project
    template_name = 'tasks/project_delete.html'

    def get_success_url(self):
        messages.add_message(self.request, messages.INFO, 'Success: Project was deleted.')
        return reverse('tasks:project_list')

    def test_func(self):
        pr = self.get_object()
        if self.request.user == pr.user or self.request.user.is_superuser:
            return True
        return False
