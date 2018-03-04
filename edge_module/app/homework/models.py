import datetime
import json
from flask import current_app
from app import db, bcrypt
from sqlalchemy.sql.schema import PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base

#Import from auth module
from app.mod_auth.models import *
from app.slides.models import *
from app.class_subject.models import * 

Base = declarative_base()



class Homework(db.Model, Base):
	__tablename__ = 'homework'
	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	class_id = db.Column(db.Integer(), db.ForeignKey('class.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
	subject_id = db.Column(db.Integer(), db.ForeignKey('subjects.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
	module_id = db.Column(db.Integer(), db.ForeignKey('module.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False) 
	chapter_id = db.Column(db.Integer(), db.ForeignKey('chapters.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
	subchapter_id = db.Column(db.Integer(), db.ForeignKey('subchapters.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=True)
	created_by = db.Column(db.Integer(), db.ForeignKey('users.id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
	homework_date = db.Column(db.String())
	created_date = db.Column(db.DateTime(), nullable=False)

	def __init__(self, class_id=None, subject_id=None, module_id=None, chapter_id=None, subchapter_id=None, created_by=None, homework_date=None, created_date=datetime.datetime.utcnow()):
		self.class_id = class_id
		self.subject_id = subject_id
		self.module_id = module_id
		self.chapter_id = chapter_id
		self.subchapter_id = subchapter_id
		self.created_by = created_by
		self.homework_date = homework_date
		self.created_date = created_date

	def __repr__(self):
		return "%s-%s-%s" %(self.id, self.created_by, self.homework_date)


class Questions(db.Model, Base):
	__tablename__ = 'questions'
	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	question = db.Column(db.Text())
	homework_id = db.Column(db.Integer(), db.ForeignKey('homework.id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
	published = db.Column(db.Boolean(), default=False)

	def __init__(self, question=None, homework_id=None, published=None):
		self.question = question
		self.homework_id=homework_id
		self.published = published

	def __repr__(self):
		return "%s-%s-%s" %(self.id, self.question, self.homework_id)

class Answers(db.Model):
	__tablename__ = 'answers'

	id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
	answer = db.Column(db.Text())
	question_id = db.Column(db.Integer(), db.ForeignKey('questions.id'))

	def __init__(self, answer=None, question_id=None, status=None):
		self.answer = answer
		self.question_id=question_id

	def __repr__(self):
		return "%s-%s-%s"%(self.id, self.answer, self.question_id)




