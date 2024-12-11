from flask import Blueprint

default_blueprint = Blueprint('default', __name__)

from app.default import routes
