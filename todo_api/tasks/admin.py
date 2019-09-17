from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ['title', 'user']
    prepopulated_fields = {'slug':('title',)}