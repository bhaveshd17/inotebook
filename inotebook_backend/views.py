import jwt
from django.contrib.auth.models import User
from django.http import JsonResponse
import json

from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed

secret = 'BhAvEsHIsGoOdBoY'




def viewData(request):
    user = User.objects.all()
    serializer = UserSerializer(user, many=True)
    return JsonResponse(serializer.data, safe=False)

def notes(request):
    return JsonResponse({'name':'notes'}, safe=False)




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
                    payload = {
                        'user_id': user.id,
                        'username': user.username
                    }

                    authToken = jwt.encode(payload, secret, algorithm='HS256').encode('utf-8')
                    response = Response()
                    response.set_cookie(key='authToken', value=authToken, httponly=True)
                    response.data = {
                        'authToken': authToken
                    }

                    return response
                else:
                    res = {"password": ["password should has minimum 8 character"]}
            else:
                res = {"password": ["password and conform password should be same"]}

        else:
            print(serialized_data.errors)
            res = serialized_data.errors

        return Response(res)


class LoginUser(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed("User not found")
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect Password")

        payload = {
            'user_id': user.id,
            'username': user.username
        }

        authToken = jwt.encode(payload, secret, algorithm='HS256').encode('utf-8')
        response = Response()
        response.set_cookie(key='authToken', value=authToken, httponly=True)
        response.data = {
            'authToken': authToken
        }

        return response

