from flask import Blueprint

customer_blueprint = Blueprint('customer', __name__)

from app.customer import routes
