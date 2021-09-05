from django.urls import path
from .views import *
urlpatterns = [
    path('getUser/', getUser, name='getUser'),
    path('allNotes/', allNotes, name='allNotes'),
    path('createNote/', createNote, name='createNote'),
    path('editNote/<str:p_key>/', editNote, name='editNote'),
    path('deleteNote/<str:p_key>/', deleteNote, name='deleteNote'),


    path('auth/createUser/', CreateUser.as_view()),
    path('auth/login/', LoginUser.as_view()),
    path('auth/logout/', LogoutUser.as_view()),
]
