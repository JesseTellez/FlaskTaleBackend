from app.models import db
from datetime import datetime

__all__ = ['Addition']

class Addition(db.Model):
    __tablename__ = 'additions'
    #NOTE - whenever you upvote an addition, that addition has to be re-evaluated.....check against other additions within that story within that indexRef
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    story_id = db.Column(db.Integer, db.ForeignKey('stories.id'))
    parent_id = db.Column(db.Integer, db.ForeignKey('additions.id'))
    #book_marks = db.Column(db.Integer, default=0)
    index_reference = db.Column(db.Integer)
    #if indexRef is None, the is_base = True
    '''To query the base I just have to query when the index_reference is null for a give story'''
    #is_base = db.Column(db.Boolean, default=False)
    #I dont think i need this yet...
    #is_active = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.Date, default=datetime.now())
    updated_at = db.Column(db.Date, default=datetime.now())
    #have to understand the parent id stuff.....
    parent_reference = db.relationship('Addition', remote_side=[id])
    #might not need this since I use a backref
    #story = db.relationship('Story', foreign_keys=story_id)
    
    def to_json(self):
        return {
            'id': self.id,
            'content': self.content,
            'parent_reference': self.parent_reference,
            #'book_marks': self.book_marks,
            'index_reference': self.index_reference,
            'updated_at': self.updated_at
        }
        
    def calculate_index_ref(self):
        if self.parent_reference is not None:
            return self.parent_reference.indexReference + 1
        return 0
        
    def make_addition_active(self):
        #what indexref are we?
        pass