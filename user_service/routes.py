from pyramid.config import Configurator

def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('register', '/api/users/register')
    config.add_route('login', '/api/users/login')  # Add this line

    config.add_route('profile', '/api/users/profile')  # Add a protected route