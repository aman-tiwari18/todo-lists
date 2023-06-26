from django.urls import path
from .views import *

urlpatterns = [
    path("register", RegisterAPIView.as_view(), name="Register"),
    path("login", LoginAPIView.as_view(), name="Login"),
    path("todo-list/<int:id>", SingleTodoListAPIView.as_view(), name="Todo List"),
    path("todo-list", TodoListAPIView.as_view(), name="Todo Lists"),
    path("task/<int:id>", TaskAPIView.as_view(), name="Task"),
]
