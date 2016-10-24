##STORY
import datetime
from app.models import db

__all__ = ['Story']

class Story(db.Model):
    __tablename__ = 'stories'
    
    '''when creating a story, you must fill out all fields that it has a foriegn relationship to...
        the story needs to know where its from/who it belongs to
        
        ex:
            story_ex = Story(name="test", owner=example_owner, genre=example_genre)
            
        to use the "many" property:
            r = Story.query.all()
            r.additions.all() -> returns all the additions
        
        '''
    
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))
    title = db.Column(db.String(200))
    is_trending = db.Column(db.Boolean, default=False)
    #This data below can also be normalized a bit better
    #number_of_additions = db.Column(db.Integer, nullable=False, default=0)
    #number_of_bookmarks = db.Column(db.Integer, nullable=False, default=0)
    #THIS RELIES ON IF THERE ARE ADDITIONS
    unique_indicies = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.now())
    
    #RELATIONS - ONE TO ONE
    #base
    #RELATIONS - BELONGS TO
    #owner = db.relationship('User')
    #genre = db.relationship('Genre')
    
    #RELATIONS - HAS MANY
    #this accounts for both active additions and regular additions, just depends on how you query
    ''' backref means you create a virtual column in the addition class that references the story
        lazy - enables you to do Story.additions (returns a query that allows to search through all the additions the story has)
        ex:
                
    '''
    additions = db.relationship('Addition', backref='story', lazy='dynamic', cascade='all')
    
    def to_json(self, base=None, adds=None):
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'genre_id': self.genre_id,
            'title': self.title,
            'is_trending': self.is_trending,
            'number_of_additions': self.query_additions,
            'number_of_bookmarks': self.query_bookmarks,
            'unique_indicies_count': self.unique_indicies,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'base': base,
            #this may not need to be an array
            'additions': [self.additions]
        }
    def to_feed_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'number_of_bookmarks': self.number_of_bookmarks
            #add number of readers
        }
        
    #Any Functions the Story Object may need
    def make_trending(self):
        pass
        
    def query_number_of_additions(self):
        pass
    
    @classmethod
    def get_story_by_id(cls, id):
        return cls.query.filter(id=id).first()
    
