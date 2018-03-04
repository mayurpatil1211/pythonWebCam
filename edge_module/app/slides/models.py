import datetime
import json
from flask import current_app
from app import db, bcrypt
from sqlalchemy.sql.schema import PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base

#Import from auth module
from app.mod_auth.models import *
from app.class_subject.models import *
from app.homework.models import *

Base = declarative_base()


class Slides(db.Model):
	__tablename__ = 'slides'

	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	heading = db.Column(db.String(), nullable=False)
	contents = db.Column(db.Text())
	slide_number = db.Column(db.Integer(), nullable=False)
	nestnumber = db.Column(db.Integer(), nullable=False)
	transition = db.Column(db.String(), nullable=True)
	backgroundColor = db.Column(db.String(), nullable=True)
	subchapter_id = db.Column(db.Integer(), db.ForeignKey('subchapters.id'), nullable=False)

	def __init__(self, heading = None, contents=None, slide_number=None, nestnumber=None, transition=None, backgroundColor=None, subchapter_id=None):
		self.heading = heading
		self.contents = contents
		self.slide_number = slide_number
		self.nestnumber = nestnumber
		self.transition = transition
		self.backgroundColor = backgroundColor
		self.subchapter_id = subchapter_id

	def __repr__(self):
		return "%s-%s" %(self.id, self.heading, self.chapter_id)


class User_slides(db.Model):
	__tablename__ = 'user_slides_completion_status_table'

	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	sid = db.Column(db.Integer(), db.ForeignKey('slides.id'), nullable=False)
	uid = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)
	date = db.Column(db.String(), nullable=True)
	status = db.Column(db.Boolean(), default=True)

	def __init__(self, sid=None, uid=None, date=None, status=None):
		self.sid = sid
		self.uid = uid
		self.date = date
		self.status = status

	def __repr__(self):
		return "%s-%s" %(self.id, self.status)