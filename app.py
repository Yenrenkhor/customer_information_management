from flask import Flask
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

from customer_information.customer_model import customer_db
from customer_information.customer_controller import customer_blueprint
from user_authentication.user_model import user_db
from user_authentication.user_controller import user_auth_blueprint

import os

load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['POSTGRES_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'admin'
jwt = JWTManager(app)

# Initialize the database
customer_db.init_app(app)
user_db.init_app(app)

# Register blueprints (views)
app.register_blueprint(user_auth_blueprint, url_prefix='/user')
app.register_blueprint(customer_blueprint, url_prefix='/customer')


if __name__ == '__main__':
    with app.app_context():
        # Create the database tables
        customer_db.create_all()
        user_db.create_all()
    app.run(port=8080)
