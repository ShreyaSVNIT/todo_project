from django import forms
from .models import Task

'''
task form has only two fields to be filled out, rest two are automatic.
'''
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'})  # 👈 HTML5 date picker
        }
