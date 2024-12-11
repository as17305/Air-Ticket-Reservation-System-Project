from flask import Blueprint

staff_blueprint = Blueprint('staff', __name__)

from app.staff import routes
