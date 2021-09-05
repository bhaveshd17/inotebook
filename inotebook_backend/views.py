import os

import jwt
from django.contrib.auth.models import User
from django.http import JsonResponse
import json

from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from .decorators import unauthenticated_user
from .utils import jwtAuthToken

secret = str(os.getenv('SECRET_JWT'))


def viewData(request):
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    return JsonResponse(serializer.data, safe=False)

def notes(request):
    return JsonResponse({'name':'notes'}, safe=False)

@unauthenticated_user(secret=secret)
def getUser(request, response):
    user_data = response['response']
    status = response['status']

    return JsonResponse(user_data, status=status)






# Authentication
class CreateUser(APIView):
    def post(self, request):
        data = json.loads(request.body)
        serialized_data = UserSerializer(data=request.data)
        if serialized_data.is_valid():
            res = serialized_data.data
            if data['password'] == data['cpassword']:
                if len(data['password']) >= 8:
                    User.objects.create_user(
                        username=res['username'],
                        email=res['email'],
                        password=data['password'],
                        first_name=res['first_name'],
                    )
                    user = User.objects.filter(username=res['username']).first()
                    response = jwtAuthToken(user, secret)
                    status = 200
                    return response
                else:
                    res = {"details": ["password should has minimum 8 character"]}
                    status = 403
            else:
                res = {"details": ["password and conform password should be same"]}
                status = 403

        else:
            print(serialized_data.errors)
            res = serialized_data.errors
            status = 403

        return Response(res, status=status)


class LoginUser(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed("User not found")
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect Password")

        response = jwtAuthToken(user, secret)
        return response


class LogoutUser(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('authToken')
        response.data = {
            "message":"logout successfully"
        }
        return response