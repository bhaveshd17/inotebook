import jwt
from django.contrib.auth.models import User
from inotebook_backend.serializers import UserSerializer


def unauthenticated_user(secret):
    def decorator(view_function):
        def wrapper_function(request, *args, **kwargs):
            token = request.COOKIES.get('authToken')
            if not token:
                res = {"user": "Unauthenticated!"}
                status = 403
                return view_function(request,{'response':res, 'status':status})
            try:
                payload = jwt.decode(token, secret, algorithms='HS256', )
                username = payload['username']
                user = User.objects.filter(username=username).first()
                serializer = UserSerializer(user)
                res = serializer.data
                status = 200
                return view_function(request, {'response': res, 'status': status})
            except Exception:
                res = {"user": "Unauthenticated!"}
                status = 403
                return view_function(request, {'response': res, 'status': status})

        return wrapper_function
    return decorator