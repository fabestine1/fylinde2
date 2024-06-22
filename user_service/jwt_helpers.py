import jwt
import time  # Import time module
from pyramid.httpexceptions import HTTPForbidden
import logging

log = logging.getLogger(__name__)

SECRET_KEY = 'mysecretkey'

def create_jwt_token(user_id, email):
    payload = {
        'sub': user_id,
        'email': email,
        'iat': int(time.time()),
        'exp': int(time.time()) + 3600
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def decode_jwt_token(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        log.info("No valid Authorization header found")
        raise HTTPForbidden(json_body={'message': 'Not authenticated'})

    token = auth_header.split(' ')[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        log.error("Token has expired")
        raise HTTPForbidden(json_body={'message': 'Token has expired'})
    except jwt.InvalidTokenError:
        log.error("Invalid token")
        raise HTTPForbidden(json_body={'message': 'Invalid token'})
