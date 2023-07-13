from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from authentications.models import CustomUser
from task.models import Task


class CreatProjectForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter name of project', 'class': 'form-control'
    }))
    description = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Describe the task', 'class': 'form-control'
    }))
    due_date = forms.CharField(widget=forms.DateInput(attrs={
        'placeholder': 'Due date', 'type': 'date','class': 'form-control'
    }))

class CreateTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'project', 'status', 'assigned_to', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class':'form-control'}),
        }
