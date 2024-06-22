from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from .models import (
    get_engine,
    get_session_factory,
    get_tm_session,
    DBSession,
    Base
)
import os
import logging

log = logging.getLogger(__name__)

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['sqlalchemy.url'] = os.environ.get('DATABASE_URL', settings['sqlalchemy.url'])
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.routes')
    config.include('pyramid_tm')

    config.scan('.views')

    engine = get_engine(settings)
    session_factory = get_session_factory(engine)
    DBSession.configure(bind=engine)

    Base.metadata.create_all(engine)

    log.info("Application setup complete")
    
    return config.make_wsgi_app()
