from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Date, Text, Boolean
from sqlalchemy.orm import relationship
from Model import Model

class Addition(Model):
    __tablename__ = 'additions'
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    content = Column(Text, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    story_id = Column(Integer, ForeignKey('stories.id'), nullable=False)
    book_marks = Column(Integer, nullable=False, default=0)
    indexReference = Column(Integer, nullable=False)
    is_base = Column(Boolean, nullable=False, default=False)
    created_at = Column(Date, nullable=False, default=datetime.now())
    updated_at = Column(Date, nullable=True, default=datetime.now())
    
    #story = relationship('Story', foreign_keys=story_id)
    
    '''
    def __init__(self):
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()
    ''' 
    def to_json(self):
        return {
            'id': self.id,
            'content': self.content,
            'book_marks': self.book_marks,
            'indexReference': self.indexReference,
            'updated_at': self.updated_at
        }