##STORY

from datetime import datetime
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Numeric, Date, Text
from sqlalchemy.orm import relationship
from MyModels import Model


class Story(Model.Model):
    __tablename__ = 'stories'
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('users.id'))
    genre_id = Column(Integer, ForeignKey('genres.id'))
    title = Column(String(200), nullable=False)
    isTrending = Column(Boolean, nullable=False, default=False)
    #This data below can also be normalized a bit better
    number_of_additions = Column(Integer, nullable=False, default=0)
    number_of_bookmarks = Column(Integer, nullable=False, default=0)
    #THIS RELIES ON IF THERE ARE ADDITIONS
    unique_indicies_count = Column(Integer, nullable=False, default=0)
    created_at = Column(Date, nullable=False, default=datetime.now())
    updated_at = Column(Date, nullable=True, default=datetime.now())
    
    #RELATIONS - ONE TO ONE
    #base
    #RELATIONS - BELONGS TO
    owner = relationship('User')
    genre = relationship('Genre')
    
    #RELATIONS - HAS MANY
    additions = relationship('Addition', backref='story', cascade='all', lazy='dynamic')
    '''
    def __init__(self):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        #This may be incorrect because we don't want user to take owner ship of others stories
        self.owner_id = 40392
    '''
    
    '''possibly have a method in here that makes a story trending depending on how much
    traffic it receives'''
    
    def to_json(self, base=None, adds=None):
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'genre_id': self.genre_id,
            'title': self.title,
            'isTrending': self.isTrending,
            'number_of_additions': self.number_of_additions,
            'number_of_bookmarks': self.number_of_bookmarks,
            'unique_indicies_count': self.unique_indicies_count,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'base': base,
            'additions': adds
        }
    def to_feed_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'number_of_bookmarks': self.number_of_bookmarks
            #add number of readers
        }
    
    @property
    def editable(self):
        current_user = "Jesse"
        if not current_user:
            return False
        #if current_user.id != self.user_id:
           # return False
        return True
        
class StoryBookmark(Model.Model):
    #this works like a LIKE
    __tablename__ = 'story_bookmark'
    story_id = Column(Integer, primary_key=True, autoincrement=False)
    user_id = Column(Integer, primary_key=True, autoincrement=False)
    created_at = Column(Date, default=datetime.now())
    
    def __init__(self, story_id, user_id):
        self.story_id = story_id
        self.user_id = user_id
        
