import jwt
from rest_framework.response import Response


def jwtAuthToken(user, secret, success):
    payload = {
        'user_id': user.id,
        'username': user.username
    }
    authToken = jwt.encode(payload, secret, algorithm='HS256')
    response = Response(headers={'authToken':authToken})
    success=True
    # response.set_cookie(key='authToken', value=authToken, httponly=True, expires=5*60*60*60)
    response.data = {
        'success':success,
        'authToken': authToken
    }
    return response