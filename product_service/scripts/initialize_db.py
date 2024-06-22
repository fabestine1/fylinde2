import os
import sys
from sqlalchemy.exc import IntegrityError
from pyramid.paster import get_appsettings, setup_logging
from ..models import (
    DBSession,
    Base,
    Product,
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

    # Add initial products
    if not session.query(Product).first():
        product = Product(name='Sample Product', description='This is a sample product', price=9.99, category='Sample Category', stock_quantity=100, image_url='')
        session.add(product)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            print("Product with this name already exists.")
