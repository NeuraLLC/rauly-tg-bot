from sqlalchemy import create_all, Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import datetime

Base = declarative_base()

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    tg_id = Column(String, unique=True)
    title = Column(String)
    username = Column(String)
    last_scanned = Column(DateTime)
    
    admins = relationship("AdminRole", back_populates="group")

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    tg_id = Column(String, unique=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    
    admin_roles = relationship("AdminRole", back_populates="user")

class AdminRole(Base):
    __tablename__ = 'admin_roles'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    role = Column(String) # e.g., 'creator', 'admin'
    custom_title = Column(String)
    
    group = relationship("Group", back_populates="admins")
    user = relationship("User", back_populates="admin_roles")

engine = create_engine('sqlite:///rauly.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def get_session():
    return Session()
