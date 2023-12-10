from django.db import models
from django.utils import timezone # для получения даты создания todo
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model): # Таблица категории, которая наследует models.Model
    name = models.CharField(max_length=155) # имя категории

    class Meta:
        verbose_name = ('Category') # для удобного чтения
        verbose_name_plural = ('Categories') # для удобного чтения в множественном числе

    def __str__(self):
        return self.name # str для отображения объекта в интерфейсе
    
class TodoList(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField(blank=True) # текстовое поле
    category = models.ForeignKey(Category, default='general', on_delete=models.PROTECT) # foreingkey нужен для связи todo c Сategory
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title