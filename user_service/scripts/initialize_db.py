import os
import sys
from sqlalchemy.exc import IntegrityError  # Ensure this import is present
from pyramid.paster import get_appsettings, setup_logging
from ..models import (
    DBSession,
    Base,
    User,
    get_engine,
)

def main(argv=sys.argv):
    if len(argv) != 2:
        sys.exit(f'Usage: {os.path.basename(argv[0])} <config_uri>\n'
                 f'(example: "{os.path.basename(argv[0])} development.ini")')
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri)

    engine = get_engine(settings)
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    session = DBSession()

    # Add initial user
    user = session.query(User).filter_by(email='admin@example.com').first()
    if not user:
        user = User(name='admin', email='admin@example.com', password='admin')
        session.add(user)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            print("User with this email already exists.")
