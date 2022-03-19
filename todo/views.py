from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from .serializers import *
from .models import *
from .token import new_access
from .service import *


class RegistrationSuperUserView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    service_class = SuperUserService

    def post(self, request):
        user = request.data
        user_data = self.service_class().registration(user)
        return Response(user_data, status=status.HTTP_201_CREATED)


class RegistrationView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    service_class = UserService

    def post(self, request):
        user = request.data
        user_data = self.service_class().registration(user)
        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    service_class = UserService

    def post(self, request):
        try:
            user = request.data
            user_data = self.service_class().login(user)
            return Response(user_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"isAuth": ""}, status=status.HTTP_401_UNAUTHORIZED)

class IsAuthView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    service_class = UserService
    def get(self, request):
        try:
            token = request.headers["Authorization"]
            result = self.service_class().is_auth(token)
            if result:
                return Response({"isAuth": result}, status=status.HTTP_200_OK)
            else:
                return Response({"isAuth": result}, status=status.HTTP_401_UNAUTHORIZED)
        except:
            return Response({"isAuth": False}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    service_class = UserService

    def get(self, request):
        try:
            token = request.headers["Authorization"]
            self.service_class().logout(token)
            return Response({"msg": "User was logout!!!!"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({"isAuth": False}, status=status.HTTP_401_UNAUTHORIZED)


class RefreshTokenView(generics.GenericAPIView):
    def get(self, request):
        token = request.COOKIES['refresh']
        if token:
            access = new_access(token)
            return Response({"access": access}, status=status.HTTP_200_OK)


class TaskView(APIView):
    permission_classes = [IsAuthenticated]
    service_class = TaskService

    def get(self, request, id):
        result = self.service_class().completed_task(id)
        return Response(result, status=status.HTTP_200_OK)

    def post(self, request):
        result = self.service_class().add_task(request.data)
        return Response(result, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        result = self.service_class().move_task(pk, request.data)
        return Response(result, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        result = self.service_class().remove_task(pk)
        return Response(result, status=status.HTTP_200_OK)


class TaskGroupView(APIView):
    permission_classes = [IsAuthenticated]
    service_class = TaskService

    def get(self, request):
        pass

    def post(self, request):
        result = self.service_class().add_task_group(request.data)
        return Response(result, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        result = self.service_class().remove_task_group(pk)
        return Response(result, status=status.HTTP_200_OK)


class TaskGroupAndTaskView(APIView):
    permission_classes = [IsAuthenticated]
    service_class = TaskService

    def get(self, request):
        result = self.service_class().get_task()
        return Response(result, status=status.HTTP_200_OK)
