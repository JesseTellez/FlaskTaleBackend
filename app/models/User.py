from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#might not need this import below
from flask import current_app
from app.models import db
from flask.ext.login import UserMixin


#In the case of the profile/managing stories, the user it the PARENT table

class UserStoryBookmark(db.Model):
    __tablename__ = 'user_story_bookmark'
    user_id = db.Column(db.Integer, db.ForiegnKey('users.id'), primary_key=True)
    story_id = db.Column(db.Integer, db.ForiegnKey('stories.id'), primary_key=True)
    timestamp = db.Column(db.Datetime, default=datetime.utcnow)
    
class UserAdditionBookmark(db.Model):
    __tablename__ = 'user_addition_bookmark'
    user_id = db.Column(db.Integer, db.ForiegnKey('users.id'), primary_key=True)
    addition_id = db.Column(db.Integer, db.ForiegnKey('additions.id', primary_key=True))
    timestamp = db.Column(db.Datetime, default=datetime.utcnow)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    #confirmed = db.Column(db.Boolean, default=False)
    location = db.Column(db.String(254))
    bio = db.Column(db.Text())
    created_at = db.Column(db.Datetime, default=datetime.utcnow)
    updated_at = db.Column(db.Datetime, default=datetime.utcnow)
    
    #deal with this later
    #profile_picture_hash = db.Column(db.String(32))
    
    bookmarked_additions = db.relationship('UserAdditionBookmark', foreign_keys = [UserAdditionBookmark.addition_id], backref=db.backref('follower', lazy='joined'), lazy='dynamic', cascade='all')
    bookmarked_stories = db.relationship('UserStoryBookmark', foreign_keys = [UserStoryBookmark.story_id], backref=db.backref('follower', lazy='joined'), lazy='dynamic', cascade='all')
    #REFERENCE - STORY = HAS MANY (PARENT)
    stories = db.relationship("Story", backref='owner', lazy='dynamic')
    #REFERENCE - ADDITION = HAS MANY
    additions = db.relationship("Addition", lazy='dynamic')
   
    def to_json(self):
       return {
        
       }
   
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash.encode('utf-8'), password.encode('utf-8'))
   
    #For email authentication and token generations 
    def generate_confirmation_token(self, expiration=3000):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})
        
        
    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True
        
    def bookmark_story(self, story):
        if not self.is_bookmarked(story):
            bm = UserStoryBookmark(followed=story)
            self.bookmarked_stories.append(bm)
    def unbookmark_story(self, story):
        bm = self.bookmarked_stories.filter_by(story_id=story.id).first()
        if bm:
            self.bookmarked_stories.remove(bm)
        
    def __repr__(self):
        return 'User %r' % self.username