from ast import Try
from linecache import cache
from turtle import title
from .serializers import *
from .models import *


class SuperUserService():
    serializer_class = RegistrationSuperUserSerializer

    def registration(self, user):
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data


class UserService():
    serializer_reg = RegistrationsSerializer
    serializer_login = LoginSerializer
    serializer_logout = LogoutSerializer

    def registration(self, user):
        serializer = self.serializer_reg(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data

    def login(self, user):
        serializer = self.serializer_login(data=user)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.data
        user_id = user_data['id']
        refresh_token = user_data['refresh']
        token = Token.objects.filter(user_id=user_id)
        if token:
            token_ = Token.objects.filter(
                user_id=user_id).update(token=refresh_token)
        else:
            token_ = Token.objects.create(token=refresh_token, user_id=user_id)
            token_.save()
        return {"access": user_data['access']}

    def is_auth(self, token):
        payload = token_decode(token.split()[1])
        token = Token.objects.get(user_id=payload["id"])
        if token:
            payload_refresh = token_decode(token.token)
            if payload_refresh["id"] == payload["id"]:
                return True
            else:
                return False

    def logout(self, token):
        payload = token_decode(token.split()[1])
        token = Token.objects.filter(user_id=payload["id"]).update(token="")


class TaskService():
    serializer_class = TaskSerializer

    def get_task(self) -> dict():
        tasks = Task.objects.all().select_related("group")
        count = TaskGroup.objects.count()
        serializer = self.serializer_class(tasks)
        serializer.get_group_task()
        if len(serializer.data) < count:
            group = TaskGroup.objects.all()
            serializer.data = serializer.add_group_task(serializer.data, group)
        self.insertionSort(serializer.data)
        return serializer.data

    def add_task(self, obj):
        task = Task.objects.create(**obj)
        task.save()
        return {"msg": "Task added success!!!!"}

    def add_task_group(self, obj):
        if obj["for_completed"] == True:
            group = TaskGroup.objects.filter(for_completed=True)
            if group:
                return {"msg": "Task Group exist!!!!"}
            else:
                group = TaskGroup.objects.create(**obj)
                group.save(group)
        else:
            group = TaskGroup.objects.create(**obj)
            group.save()
        return {"msg": "Task Group added success!!!!"}

    def remove_task_group(self, _id):
        try:
            TaskGroup.objects.filter(id=_id).delete()
            return {"msg": "Task Group added success!!!!"}
        except:
            print("An exception occurred")

    def remove_task(self, _id):
        try:
            Task.objects.filter(id=_id).delete()
            return {"msg": "Task Group added success!!!!"}
        except:
            print("An exception occurred")

    def move_task(self, _id, body):
        try:
            Task.objects.filter(id=_id).update(**body)
            return {"msg": "Task Group added success!!!!"}
        except:
            print("An exception occurred")

    def completed_task(self, _id):
        try:
            try:
                group = TaskGroup.objects.filter(for_completed=True)
            except Exception as e:
                print(e)
            if group:
                Task.objects.filter(id=_id).update(is_completed=True, group_id=group[0].id)
                return {"msg": "Task was completed!!!!"}
            else:
                print("group")
                group = TaskGroup.objects.create(title="Completed", for_completed=True)
                
                group.save()
                Task.objects.filter(id=_id).update(is_completed=True, group_id=group.id)
                return {"msg": "Task was completed!!!!"}
        except:
            print("An exception occurred")

    def insertionSort(self, arr):
        key = 0
        j = 0
        for i in range(len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j]['id'] > key['id']:
                arr[j + 1] = arr[j]
                j = j - 1
            arr[j + 1] = key
        return arr
