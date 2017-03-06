
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context
from .config import Config

db = SQLAlchemy()

class UserModel(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key = True)
	email = db.Column(db.String(250), nullable=False)
	password = db.Column(db.String(250), nullable=False)

	def __init__(self, email, password):
		self.email = email
		self.password = pwd_context.encrypt(password)
	
	def verify_password(self, password):
		return pwd_context.verify(password, self.password)

	def generate_auth_token(self, expiration = 3600):
		s = Serializer(Config.SECRET_KEY, expires_in = expiration)
		return s.dumps({ 'id': self.id })

	@staticmethod
	def verify_auth_token(token):
		s = Serializer(Config.SECRET_KEY)
		try:
			data = s.loads(token)
		except SignatureExpired:
			return None # valid token, but expired
		except BadSignature:
			return None # invalid token
		user = UserModel.query.get(data['id'])
		return user

class BucketListModel(db.Model):
	__tablename__ = 'bucketlist'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(250), nullable=False)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),onupdate=db.func.current_timestamp())
	created_by = db.Column(db.String(250), nullable=False)
	items = relationship("ItemsModel", back_populates="bucketlist")
	
class ItemsModel(db.Model):
	__tablename__ = 'items'
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(250), nullable=False)
	date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
	date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),onupdate=db.func.current_timestamp())
	done = db.Column(db.Boolean, default=True)
	bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id'))
	bucketlist = relationship("BucketListModel", back_populates="items")
	
