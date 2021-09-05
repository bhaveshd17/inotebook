import jwt
from rest_framework.response import Response


def jwtAuthToken(user, secret):
    payload = {
        'user_id': user.id,
        'username': user.username
    }
    authToken = jwt.encode(payload, secret, algorithm='HS256')
    response = Response()
    response.set_cookie(key='authToken', value=authToken, httponly=True, expires=24 * 60 * 60)
    response.data = {
        'authToken': authToken
    }
    return response