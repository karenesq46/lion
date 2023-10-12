from django import forms
from .models import Profile, Task


class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['name', 'phone', 'email', 'status', 'photo']
        
class TaskForm(forms.ModelForm):
    class Meta:
        model=Task
        fields=['title', 'description', 'important']