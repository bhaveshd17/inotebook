import jwt
from django.contrib.auth.models import User
from inotebook_backend.serializers import UserSerializer

def unauthenticated_user(secret):
    def decorator(view_function):
        def wrapper_function(request, p_key=None, *args, **kwargs):
            try:
                token = request.headers.get('authToken')
                payload = jwt.decode(token, secret, algorithms='HS256', )
                username = payload['username']
                user = User.objects.filter(username=username).first()
                serializer = UserSerializer(user)
                response = serializer.data
                status = 200
                return view_function(request, {'response':response, 'status':status}, p_key)
            except jwt.InvalidTokenError as err:
                print(err)
                response = "Unauthenticated"
                status = 401
                return view_function(request, {'response':response, 'status':status}, p_key)
            except Exception as e:
                print(e)
                response = "Internal Server Error"
                status = 500
                return view_function(request, {'response': response, 'status': status}, p_key)

        return wrapper_function
    return decorator

