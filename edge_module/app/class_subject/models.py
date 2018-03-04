import datetime
import json
from flask import current_app
from app import db, bcrypt
from sqlalchemy.sql.schema import PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base

#Import from auth module
from app.mod_auth.models import *
from app.slides.models import *
from app.homework.models import *

Base = declarative_base()

#association Table
class_subject_table = db.Table('class_subject_table',
    db.Column('class_id', db.Integer, db.ForeignKey('class.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
    db.Column('subject_id', db.Integer, db.ForeignKey('subjects.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False),
    db.PrimaryKeyConstraint('class_id', 'subject_id')
    )




class Classes(db.Model, Base):
    __tablename__='class'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_name = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=True)

    class_subjects = db.relationship('Subjects', secondary=class_subject_table, backref=db.backref('class', lazy='dynamic'))

    def __init__(self, class_name=None, status='Active'):
        self.class_name= class_name
        self.status= status

    def __repr__(self):
        return "%s-%s" %(self.id, self.class_name)


class Subjects(db.Model, Base):
	__tablename__ = 'subjects'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	subject_name = db.Column(db.String, nullable=False)

	def __init__(self, subject_name=None):
		self.subject_name = subject_name

	def __repr__(self):
		return "%s-%s" %(self.id, self.subject_name)



class Modules(db.Model):
	__tablename__ = 'module'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	module_name = db.Column(db.String, nullable=False)
	url = db.Column(db.String, nullable=True)
	subject_id = db.Column(db.Integer(), db.ForeignKey('subjects.id'))
	class_id = db.Column(db.Integer(), db.ForeignKey('class.id'))

	def __init__(self,module_name=None, url=None, subject_id=None, class_id=None):
		self.module_name = module_name
		self.url = url
		self.subject_id = subject_id
		self.class_id = class_id

	def __repr__(self):
		return "%s-%s" %(self.id, self.module_name)


class Chapters(db.Model):
	__tablename__ = 'chapters'

	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	chapter_name = db.Column(db.String(), nullable=False)
	url = db.Column(db.String(), nullable=True)
	published = db.Column(db.Boolean, default=False)
	completed = db.Column(db.Boolean, default=False)
	select_date = db.Column(db.String(), nullable=False)
	module_id = db.Column(db.Integer(), db.ForeignKey('module.id'))

	def __init__(self, chapter_name=None, url=None, published=None, completed=None, select_date=None, module_id=None):
		self.chapter_name=chapter_name
		self.url = url
		self.published = published
		self.completed = completed
		self.select_date = select_date
		self.module_id = module_id

	def __repr__(self):
		return "%s-%s" %(self.id, self.chapter_name)

class Subchapters(db.Model):
	__tablename__ = 'subchapters'

	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	name = db.Column(db.String(), nullable=False)
	url = db.Column(db.String(), nullable=True)
	published = db.Column(db.Boolean(),default=False)
	completed = db.Column(db.Boolean(), default=False)
	select_date = db.Column(db.String(), nullable=False)
	chapter_id = db.Column(db.Integer(), db.ForeignKey('chapters.id'))

	def __init__(self, name=None, url=None, published=None, completed=None, select_date=None, chapter_id=None):
		self.name = name
		self.url = url
		self.published = published
		self.completed = completed
		self.select_date = select_date
		self.chapter_id = chapter_id

	def __repr__(self):
		return "%s-%s" %(self.id, self.name)


