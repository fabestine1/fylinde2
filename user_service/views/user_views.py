from pyramid.view import view_config
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound, HTTPForbidden
from pyramid.security import remember, forget
from pyramid.response import Response
from ..models import DBSession, User
from ..jwt_helpers import create_jwt_token, decode_jwt_token
import bcrypt
import logging

log = logging.getLogger(__name__)

@view_config(route_name='register', renderer='json', request_method='POST')
def register_view(request):
    try:
        data = request.json_body
        name = data['name']
        email = data['email']
        password = data['password']
    except KeyError as e:
        return HTTPBadRequest(json_body={'message': f'Missing parameter: {str(e)}'})

    existing_user = DBSession.query(User).filter_by(email=email).first()
    if existing_user:
        return HTTPBadRequest(json_body={'message': 'User with this email already exists'})

    hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    user = User(name=name, email=email, password=hashed_password.decode('utf8'))
    DBSession.add(user)
    DBSession.flush()
    DBSession.commit()

    log.info(f"User registered: {user.email}")
    return {'message': 'User registered successfully'}

@view_config(route_name='login', renderer='json', request_method='POST')
def login_view(request):
    try:
        data = request.json_body
        email = data['email']
        password = data['password']
    except KeyError as e:
        return HTTPBadRequest(json_body={'message': f'Missing parameter: {str(e)}'})

    user = DBSession.query(User).filter_by(email=email).first()
    if not user or not bcrypt.checkpw(password.encode('utf8'), user.password.encode('utf8')):
        return HTTPNotFound(json_body={'message': 'Invalid username or password'})

    token = create_jwt_token(user.id, user.email)
    headers = remember(request, token)
    log.info(f"Login successful for user: {user.email}")
    return {'message': 'Login successful', 'user': user.email, 'token': token}

@view_config(route_name='profile', renderer='json', request_method='GET', permission='authenticated')
def profile_view(request):
    try:
        claims = decode_jwt_token(request)
        user_id = claims.get('sub')
        if not user_id:
            log.error("No user ID found in token claims")
            return HTTPForbidden(json_body={'message': 'Not authenticated'})

        user = DBSession.query(User).filter_by(id=user_id).first()
        if not user:
            log.error(f"No user found with ID: {user_id}")
            return HTTPNotFound(json_body={'message': 'User not found'})

        log.info(f"Profile accessed for user: {user.email}")
        return {'name': user.name, 'email': user.email}
    except HTTPForbidden as e:
        return e
