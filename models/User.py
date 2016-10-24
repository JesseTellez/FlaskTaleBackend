##USER
import time
import uuid
from datetime import datetime
from flask import request, session, current_app
from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Date, Boolean, Text
from sqlalchemy.orm import relationship
from Model import Model

#In the case of the profile/managing stories, the user it the PARENT table

class User(Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(64))
    user_password = Column(String(128))
    user_email = Column(String(64))
    user_location = Column(String(200))
    user_bio = Column(Text(1000))
    
    #REFERENCE - STORY = HAS MANY (PARENT)
    stories = relationship("Story")
    #REFERENCE - ADDITION = HAS MANY
    additions = relationship("Addition")
    
    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password = password
        
    #flask login information
    def is_authenticated(self):
        return True
        
    def is_active(self):
        return True
        
    def is_anon(self):
        return False
        
    def get_id(self):
        return self.user_id
        
    def __unicode__(self):
        return self.user_name
        
        
        
        
    