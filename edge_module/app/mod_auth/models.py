# project/api/models.py


import datetime
import json
import jwt
from flask import current_app
from app import db, bcrypt
from sqlalchemy.sql.schema import PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base

#import from class_subject Module
from app.class_subject.models import *
from app.slides.models import *
from app.homework.models import *


Base = declarative_base()


#Association Table
class_user_table = db.Table('class_user_table',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
    db.Column('class_id', db.Integer, db.ForeignKey('class.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
    db.PrimaryKeyConstraint('user_id', 'class_id')
    )








#Base Tables
class User(db.Model, Base):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(128), unique=False, nullable=True)
    last_name = db.Column(db.String(128), unique=False, nullable=True)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    admin = db.Column(db.Boolean, default=False, nullable=False)
    user_roles_id = db.Column(db.Integer, db.ForeignKey('user_roles.id'))
    created_at = db.Column(db.DateTime, nullable=False)

    class_users = db.relationship('Classes', secondary=class_user_table, backref=db.backref('users', lazy='dynamic'))

    def __init__(self,first_name, last_name, email, password, user_roles_id, created_at = datetime.datetime.utcnow()):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.user_roles_id = user_roles_id 
        self.created_at = created_at

    def encode_auth_token(self, user_id):
        """Generates the auth token"""
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(
                    days=current_app.config.get('TOKEN_EXPIRATION_DAYS'),
                    seconds=current_app.config.get('TOKEN_EXPIRATION_SECONDS')
                ),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """Decodes the auth token - :param auth_token: - :return: integer|string"""
        try:
            payload = jwt.decode(
                auth_token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class User_roles(db.Model):
    __tablename__ = "user_roles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(250), nullable=False)
    status = db.Column(db.String(250), nullable=False)

    def __init__(self, role_name= None, status= None):
        self.role_name = role_name
        self.status = status

    def __repr__(self):
        return "%s-%s-%s" %(self.id, self.role_name, self.status)

