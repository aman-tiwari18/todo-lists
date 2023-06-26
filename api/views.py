import json

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.status import *

from .models import *
from .serializers import *


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data: dict = json.loads(request.body)
        try:
            assert data["username"] and data["password"], KeyError()
            username = data["username"].strip()
            password = data["password"].strip()
            accounts = Account.objects.filter(username=username)
            if accounts.exists():
                return Response(
                    {"message": "Username already exists"}, status=HTTP_409_CONFLICT
                )
            account = Account.objects.create_user(
                username=username, password=password)
            token = Token.objects.create(user=account)
            token.save()
            return Response(
                {
                    "message": "Registration Successfully",
                    "token": token.key,
                    "username": account.username,
                    "id": account.id,
                },
                status=HTTP_201_CREATED,
            )
        except:
            return Response({"message": "Invalid data"}, status=HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data: dict = json.loads(request.body)
        try:
            assert data["username"] and data["password"], KeyError()
            username = data["username"].strip()
            password = data["password"].strip()
            accounts = Account.objects.filter(username=username)
            if not accounts.exists():
                return Response(
                    {"message": "Account not found"}, status=HTTP_404_NOT_FOUND
                )
            account = accounts.first()
            if not account.check_password(password):
                return Response(
                    {"error": "Invalid Credentials"}, status=HTTP_401_UNAUTHORIZED
                )
            token = Token.objects.filter(user=account).first()
            return Response(
                {
                    "message": "Login Successfully",
                    "token": token.key,
                    "username": account.username,
                    "id": account.id,
                },
                status=HTTP_200_OK,
            )
        except Exception as e:
            return Response({"message": "Invalid data"}, status=HTTP_400_BAD_REQUEST)


class SingleTodoListAPIView(APIView):
    def get(self, request, id):
        user = request.user
        todo_lists = TodoList.objects.filter(id=id, account=user)
        if not todo_lists.exists():
            return Response(
                {"message": "No List found with given ID"}, status=HTTP_404_NOT_FOUND
            )
        todo_list = todo_lists.first()
        if todo_list.account != user:
            return Response(
                {"message": "You are not permitted to view this todo list"},
                status=HTTP_403_FORBIDDEN,
            )
        tasks = Task.objects.filter(todo_list=todo_list)
        serializer = TaskSerializer(tasks, many=True)
        return Response({"data": serializer.data})

    def delete(self, request, id):
        user = request.user
        todo_list = TodoList.objects.filter(id=id, account=user)
        if not todo_list.exists():
            return Response(
                {"message": "No List found with given ID"}, status=HTTP_404_NOT_FOUND
            )
        todo_list.first().delete()
        return Response({"message": "Todo List deleted Successfully"})

    def patch(self, request, id):
        user = request.user
        todo_list = TodoList.objects.filter(id=id, account=user)
        if not todo_list.exists():
            return Response(
                {"message": "No List found with given ID"}, status=HTTP_404_NOT_FOUND
            )
        serializer = TodoListSerializer(
            todo_list.first(), data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data})
        return Response({"message": serializer.errors}, status=HTTP_400_BAD_REQUEST)


class TodoListAPIView(APIView):
    def get(self, request):
        user = request.user
        todo_list = TodoList.objects.filter(account=user)
        serializer = TodoListSerializer(todo_list, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        data = json.loads(request.body)
        serializer = TodoListSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=HTTP_201_CREATED)
        return Response({"message": serializer.errors}, status=HTTP_400_BAD_REQUEST)


class TaskAPIView(APIView):
    def has_perm(self, request, user):
        if request.user.id == user.id:
            return True
        return False

    def get(self, request, id):
        tasks = Task.objects.filter(id=id)
        if not tasks.exists():
            return Response(
                {"message": "No task found with given ID"}, status=HTTP_404_NOT_FOUND
            )
        task = tasks.first()
        if not self.has_perm(request, task.todo_list.account):
            return Response(
                {"message": "You are not permitted to view this task list"},
                status=HTTP_403_FORBIDDEN,
            )
        serializer = TaskSerializer(task)
        return Response({"data": serializer.data})

    def post(self, request, id):
        data = json.loads(request.body)
        data["todo_list"] = id
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data}, status=HTTP_201_CREATED)
        return Response({"message": serializer.errors}, status=HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        tasks = Task.objects.filter(id=id)
        if not tasks.exists():
            return Response(
                {"message": "No task found with given ID"}, status=HTTP_404_NOT_FOUND
            )
        task = tasks.first()
        if not self.has_perm(request, task.todo_list.account):
            return Response(
                {"message": "You are not permitted to edit this task list"},
                status=HTTP_403_FORBIDDEN,
            )
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data})
        return Response({"message": serializer.errors}, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        tasks = Task.objects.filter(id=id)
        if not tasks.exists():
            return Response(
                {"message": "No task found with given ID"}, status=HTTP_404_NOT_FOUND
            )
        task = tasks.first()
        if not self.has_perm(request, task.todo_list.account):
            return Response(
                {"message": "You are not permitted to edit this task list"},
                status=HTTP_403_FORBIDDEN,
            )
        task.delete()
        return Response({"message": "Task deleted Successfully"})
