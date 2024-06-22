# user_service/jwt.py
import jwt
from pyramid.request import Request

def add_jwt_claims_to_request(request: Request):
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        token = token.split('Bearer ')[1]
        try:
            claims = jwt.decode(token, 'mysecretkey', algorithms=['HS256'])
            request.jwt_claims = claims
        except jwt.InvalidTokenError:
            request.jwt_claims = None
    else:
        request.jwt_claims = None
