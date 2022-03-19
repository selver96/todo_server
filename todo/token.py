import jwt
from datetime import datetime
from datetime import timedelta
from django.conf import settings
from rest_framework import exceptions


def access(_id, name, surname, email):
    access_exp = datetime.now() + timedelta(minutes=30)
    access = jwt.encode({
        'id': _id,
        'name': name,
        'surname': surname,
        'email': email,
        'exp': int(access_exp.strftime('%s'))
    }, settings.SECRET_KEY, algorithm="HS256")
    return access


def refresh(_id, name, surname, email):
    refresh_exp = datetime.now() + timedelta(days=1)
    refresh = jwt.encode({
        'id': _id,
        'name': name,
        'surname': surname,
        'email': email,
        'exp': int(refresh_exp.strftime('%s'))
    }, settings.SECRET_KEY, algorithm="HS256")
    return refresh


def new_access(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        msg = "Signature has expired. "
        raise exceptions.AuthenticationFailed(msg)
    access = access(payload['id'],payload['name'],payload['surname'],payload['email'])
    return access

def token_decode(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        msg = "Signature has expired. "
        raise exceptions.AuthenticationFailed(msg)
    return payload