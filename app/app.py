from flask import Flask
from app.customer import customer_blueprint
from app.staff import staff_blueprint
from app.default import default_blueprint

app = Flask(__name__)
app.secret_key = 'notsosecretkey!'

app.register_blueprint(default_blueprint)
app.register_blueprint(customer_blueprint, url_prefix='/customer')
app.register_blueprint(staff_blueprint, url_prefix="/staff")