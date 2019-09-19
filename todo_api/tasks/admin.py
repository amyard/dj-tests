from django.contrib import admin
from .models import Project, Task

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title','user',)
    list_filter = ['title', 'user']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title','project', 'user', 'priority', 'status', 'created']
    list_filter = ['created', 'priority', 'status']
    list_editable = ['priority', 'status']
    date_hierarchy = 'created'

    prepopulated_fields = {'slug': ('title',)}

    fieldsets = [
        ('General Info', {'fields': ['title', 'slug']}),
        ('Content', {'fields': ['project', 'description']}),
        ('Choices', {'fields': ['priority', 'status']})
    ]

    def user(self, obj):
        return obj.project.user