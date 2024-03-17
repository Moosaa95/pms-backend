from django import forms
from .models import Project, Task


class ProjectForms(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'due_date', 'progress', 'status']


class TaskForms(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['project', 'description',  'status']