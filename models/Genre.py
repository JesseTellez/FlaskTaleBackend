from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, Numeric, Date, Text, Boolean
from sqlalchemy.orm import relationship
from Model import Model

class Genre(Model):
    
    __tablename__ = 'genres'
    
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    title = Column(String(256))
    #CODE BELOW - might want to make this refer to a foriegn key
    numberOfStories = Column(Integer, default=0)
    numberOfActiveReaders = Column(Integer, default=0)
    description = Column(Text(2000))
    created_at = Column(Date, default=datetime.now())
    updated_at = Column(Date, default=datetime.now())
    
    #Relations
    stories = relationship('Story')
    '''
    def __init__(self):
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()
     '''   
    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'numberOfStories': self.numberOfStories,
            'numberOfActiveReaders': self.numberOfActiveReaders,
            'description': self.description,
            'updated_at': self.updatedAt
        }
        
    
    def list_genres():
        genres = Genre.query.all()
        return [c.to_json() for c in genres]
        