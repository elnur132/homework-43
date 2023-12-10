from django.urls import path
from .views import TodoListView, TodoCreate, EditTodo, not_done, done, delete

app_name = 'todo'

urlpatterns = [
    path('', TodoListView.as_view(), name = 'main'),
    path('create/', TodoCreate.as_view(), name = 'create'),
    path('not_done/<task_id>', not_done, name = 'not_done'),
    path('done/<task_id>', done, name = 'done'),
    path('edit/<task_id>', EditTodo.as_view(), name = 'edit'),
    path('delete/<task_id>', delete, name = 'delete'),
]
