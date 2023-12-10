from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from .models import Category, TodoList
from .forms import TodoForm
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class TodoListView(ListView):
    model = TodoList
    template_name = 'main.html'
    context_object_name = 'todos'
    
    def get_queryset(self):
        queryset = TodoList.objects.filter(user=self.request.user.id)

        return queryset


class TodoCreate(CreateView):
    model = TodoList
    form_class = TodoForm
    template_name = 'todocreate.html'
    success_url = reverse_lazy('todo:main')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


def not_done(request, task_id):
    task = TodoList.objects.get(pk=task_id)
    task.completed = False
    task.save()
    return redirect('todo:main')

def done(request, task_id):
    task = TodoList.objects.get(pk=task_id)
    task.completed = True
    task.save()
    return redirect('todo:main')

class EditTodo(LoginRequiredMixin, UpdateView):
    model = TodoList
    form_class = TodoForm
    pk_url_kwarg = 'task_id'
    template_name = 'edit.html'
    success_url = reverse_lazy('todo:main')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].user:
            return self.handle_no_permission()
        return kwargs
    
def delete(request, task_id):
    task = TodoList.objects.get(pk=task_id)
    
    task.delete()
    return redirect('todo:main')