# Import flask and template operators
from flask import Flask, Blueprint
from flask_cors import CORS, cross_origin

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_bcrypt import Bcrypt
import jwt

# Define the WSGI application object
app = Flask(__name__)
CORS(app)

# Configurations
app.config.from_object('config.DevelopmentConfig')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import auth_blueprint
from app.class_subject.controllers import class_blueprint
from app.slides.controllers import slides_blueprint
from homework.controllers import homework_blueprint




# Register blueprint(s)
app.register_blueprint(auth_blueprint)
app.register_blueprint(class_blueprint)
app.register_blueprint(slides_blueprint)
app.register_blueprint(homework_blueprint)





db.create_all()