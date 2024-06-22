from pyramid.view import view_config
from pyramid.response import Response
from models import DBSession, User
from sqlalchemy.exc import IntegrityError
import bcrypt

@view_config(route_name='register', renderer='json', request_method='POST')
def register_view(request):
    try:
        data = request.json_body
        hashed_password = bcrypt.hashpw(data['password'].encode('utf8'), bcrypt.gensalt())
        new_user = User(name=data['name'], email=data['email'], password=hashed_password.decode('utf8'))
        DBSession.add(new_user)
        DBSession.flush()
        return Response(json_body={'message': 'User registered successfully'}, status=201)
    except IntegrityError:
        DBSession.rollback()
        return Response(json_body={'message': 'Email already exists'}, status=400)
    except Exception as e:
        return Response(json_body={'message': str(e)}, status=500)

@view_config(route_name='login', renderer='json', request_method='POST')
def login_view(request):
    data = request.json_body
    user = DBSession.query(User).filter_by(email=data['email']).first()
    if user and bcrypt.checkpw(data['password'].encode('utf8'), user.password.encode('utf8')):
        # Generate a token or a session here
        return Response(json_body={'message': 'Login successful'}, status=200)
    return Response(json_body={'message': 'Invalid email or password'}, status=400)
