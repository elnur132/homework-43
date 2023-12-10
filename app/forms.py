from django import forms
from django.forms import ModelForm
from .models import Category, TodoList

class TodoForm(ModelForm):

    class Meta:
        model = TodoList
        fields = ('title', 'content', 'category')


