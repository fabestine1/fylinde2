from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import register

DBSession = scoped_session(sessionmaker())
Base = declarative_base()

def get_engine(settings):
    from sqlalchemy import engine_from_config
    return engine_from_config(settings, 'sqlalchemy.')

def get_session_factory(engine):
    factory = sessionmaker()
    factory.configure(bind=engine)
    return factory

def get_tm_session(session_factory, transaction_manager):
    """ Get a transactional scope session.
    """
    dbsession = session_factory()
    register(dbsession, transaction_manager=transaction_manager)
    return dbsession

def includeme(config):
    settings = config.get_settings()
    config.include('pyramid_tm')
    config.include('pyramid_retry')
    engine = get_engine(settings)
    session_factory = get_session_factory(engine)
    config.registry['dbsession_factory'] = session_factory
    config.add_request_method(
        lambda r: get_tm_session(session_factory, r.tm),
        'dbsession',
        reify=True
    )
    # Import models to ensure they are registered correctly
    from .user_model import User

# Ensure this import is here
from .user_model import User
