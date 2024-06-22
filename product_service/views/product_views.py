from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest
from ..models import DBSession, Product
import logging

log = logging.getLogger(__name__)

@view_config(route_name='products', renderer='json', request_method='GET')
def get_products(request):
    products = DBSession.query(Product).all()
    return [product.to_dict() for product in products]

@view_config(route_name='product', renderer='json', request_method='GET')
def get_product(request):
    product_id = request.matchdict.get('id')
    product = DBSession.query(Product).filter_by(id=product_id).first()
    if not product:
        return HTTPNotFound(json_body={'message': 'Product not found'})
    return product.to_dict()

@view_config(route_name='products', renderer='json', request_method='POST')
def create_product(request):
    try:
        data = request.json_body
        name = data['name']
        description = data.get('description', '')
        price = data['price']
        category = data['category']
        stock_quantity = data['stock_quantity']
        image_url = data.get('image_url', '')
    except KeyError as e:
        return HTTPBadRequest(json_body={'message': f'Missing parameter: {str(e)}'})

    product = Product(
        name=name,
        description=description,
        price=price,
        category=category,
        stock_quantity=stock_quantity,
        image_url=image_url
    )
    DBSession.add(product)
    DBSession.flush()
    DBSession.commit()

    log.info(f"Product created: {product.name}")
    return {'message': 'Product created successfully', 'product': product.to_dict()}

@view_config(route_name='product', renderer='json', request_method='PUT')
def update_product(request):
    product_id = request.matchdict.get('id')
    product = DBSession.query(Product).filter_by(id=product_id).first()
    if not product:
        return HTTPNotFound(json_body={'message': 'Product not found'})

    try:
        data = request.json_body
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)
        product.category = data.get('category', product.category)
        product.stock_quantity = data.get('stock_quantity', product.stock_quantity)
        product.image_url = data.get('image_url', product.image_url)
    except KeyError as e:
        return HTTPBadRequest(json_body={'message': f'Missing parameter: {str(e)}'})

    DBSession.flush()
    DBSession.commit()

    log.info(f"Product updated: {product.name}")
    return {'message': 'Product updated successfully', 'product': product.to_dict()}

@view_config(route_name='product', renderer='json', request_method='DELETE')
def delete_product(request):
    product_id = request.matchdict.get('id')
    product = DBSession.query(Product).filter_by(id=product_id).first()
    if not product:
        return HTTPNotFound(json_body={'message': 'Product not found'})

    DBSession.delete(product)
    DBSession.flush()
    DBSession.commit()

    log.info(f"Product deleted: {product.name}")
    return {'message': 'Product deleted successfully'}
