import jwt
from django.contrib.auth.models import User
from inotebook_backend.serializers import UserSerializer


def unauthenticated_user(secret):
    def decorator(view_function):
        def wrapper_function(request, p_key=None, *args, **kwargs):
            token = request.COOKIES.get('authToken')
            if not token:
                res = "Unauthenticated"
                status = 403
                return view_function(request,{'response':res, 'status':status}, p_key)
            try:
                payload = jwt.decode(token, secret, algorithms='HS256', )
                username = payload['username']
                user = User.objects.filter(username=username).first()
                serializer = UserSerializer(user)
                res = serializer.data
                request.user = res
                status = 200
                return view_function(request, {'response': res, 'status': status}, p_key)
            except Exception:
                res = "Unauthenticated"
                status = 403
                return view_function(request, {'response': res, 'status': status}, p_key)

        return wrapper_function
    return decorator