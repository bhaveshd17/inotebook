import os

from django.contrib.auth.models import User
from django.http import JsonResponse
import json

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Notes
from .serializers import UserSerializer, NotesSerializer, AllNotesSerializer
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from .decorators import unauthenticated_user
from .utils import jwtAuthToken

secret = str(os.getenv('SECRET_JWT'))

@api_view(['POST'])
@unauthenticated_user(secret=secret)
def getUser(request, response, p_key):
    res = response['response']
    status = response['status']
    return JsonResponse(res, status=status, safe=False)


@api_view(['GET'])
@unauthenticated_user(secret=secret)
def allNotes(request, response, p_key):
    user_data = response['response']
    status = response['status']
    if  str(user_data).lower() == 'unauthenticated':
        res = {"User": "Unauthenticated"}
    else:
        user = User.objects.filter(username=user_data['username']).first()
        notes = Notes.objects.filter(user=user)
        notes_serialized_data = AllNotesSerializer(notes, many=True)
        res = notes_serialized_data.data
    return JsonResponse(res, status=status, safe=False)


@api_view(['POST'])
@unauthenticated_user(secret=secret)
def createNote(request, response, p_key):
   user_data = response['response']
   status = response['status']
   if str(user_data).lower() == 'unauthenticated':
       res = {"User": "Unauthenticated"}
   else:
       note_serializer = NotesSerializer(data=request.data)
       if note_serializer.is_valid():
          try:
              user = User.objects.filter(username=user_data['username']).first()
              Notes.objects.create(
                  user=user,
                  title=note_serializer['title'].value,
                  description=note_serializer['description'].value,
                  tags=note_serializer['tags'].value
              )
              res = note_serializer.data

          except Exception:
              res = "Internal Server Error"
              status = 500

       else:
           res = {"data": note_serializer.errors}
           status = 400
   return JsonResponse(res, status=status, safe=False)


@api_view(['POST', 'PUT'])
@unauthenticated_user(secret=secret)
def editNote(request, response, p_key):
    user_data = response['response']
    status = response['status']
    if str(user_data).lower() == 'unauthenticated':
        res = {"User": "Unauthenticated"}
    else:
        try:
            note = Notes.objects.filter(id=p_key).first()
            note_serializer = NotesSerializer(instance=note, data=request.data)
            if note_serializer.is_valid():
                note_serializer.save()
                res = note_serializer.data

            else:
                res = {"data": note_serializer.errors}
                status = 400
        except Exception:
            res = "Internal Server Error"
            status = 500
    return JsonResponse(res, status=status, safe=False)


@api_view(['DELETE'])
@unauthenticated_user(secret=secret)
def deleteNote(request, response, p_key):
    user_data = response['response']
    status = response['status']
    if str(user_data).lower() == 'unauthenticated':
        res = {"User": "Unauthenticated"}
    else:
        try:
            note = Notes.objects.filter(id=p_key).first()
            note.delete()
            res = {"message": "successfully deleted"}
        except Exception:
            res = "Internal Server Error"
            status = 500

    return JsonResponse(res, status=status, safe=False)







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
        response = Response(headers=None)
        response.data = {
            "message":"logout successfully"
        }
        return response