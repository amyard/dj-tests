from django import forms

from .models import Project

class ProjectCreateForm(forms.ModelForm):
    title = forms.CharField(label='Project', widget=forms.TextInput())

    class Meta:
        model = Project
        fields = ('title', 'color',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', '')
        super(ProjectCreateForm, self).__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data['title']
        if Project.objects.filter(title=title, user=self.user).exists():
            raise forms.ValidationError('You cann\'t use this title again.')
        return title

    def clean_color(self):
        color = self.cleaned_data['color']
        if Project.objects.filter(color=color, user=self.user).exists():
            raise forms.ValidationError('You cann\'t use this color again.')
        return color


class ProjectUpdateForm(forms.ModelForm):

    title = forms.CharField()
    color = forms.CharField()

    class Meta:
        model = Project
        fields = ['title', 'color']

    def __init__(self, *args, **kwargs):
        self.slug = kwargs.pop('slug')
        self.user = kwargs.pop('user')
        super(ProjectUpdateForm, self).__init__(*args, **kwargs)

    def clean(self):
        title = self.cleaned_data['title']
        color = self.cleaned_data['color']

        if Project.objects.exclude(slug=self.slug).filter(title=title, user = self.user).exists():
            raise forms.ValidationError('You cann\'t use this title again.')