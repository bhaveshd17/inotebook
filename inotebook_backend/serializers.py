from django.contrib.auth.models import User
from rest_framework import serializers
from inotebook_backend.models import Notes


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'date_joined', 'is_staff']

class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        exclude = ['user']

class AllNotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = '__all__'