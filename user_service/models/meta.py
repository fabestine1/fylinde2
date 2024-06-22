from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)
from zope.sqlalchemy import register

DBSession = scoped_session(sessionmaker())
Base = declarative_base()

def get_engine(settings):
    from sqlalchemy import engine_from_config
    return engine_from_config(settings, 'sqlalchemy.')
