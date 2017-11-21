from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()
class User(Base):
	__tablename__ = 'user'
	id = Column(Integer, primary_key = True)
	username = Column(String(40), index = True)
	password_hash = Column(String(120))

	def hash_password(self, password):
		self.password_hash = pwd_context.encrypt(password)

	def verify_password(self, password):
		return pwd_context.verify(password)


engine = create_engine('sqlite:///users.db')
 

Base.metadata.create_all(engine)
    
