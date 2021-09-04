from django.urls import path
from .views import *
urlpatterns = [
    path('notes/', notes, name='notes'),
    path('view/', viewData, name='view'),
    path('auth/createUser/', CreateUser.as_view()),
    path('auth/login/', LoginUser.as_view()),
]