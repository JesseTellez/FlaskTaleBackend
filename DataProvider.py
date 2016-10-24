import datetime
import time

import json

from flask import jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import and_

#the order matters here! it must match the __init__ method
from MyModels import Story
from MyModels import User
from MyModels import Genre
from MyModels import Addition
from MyModels import init_database

from redis import Redis

redis = Redis()

ONLINE_LAST_MINUTES = 5


class DataProviderService():
    '''INITAILIZATION'''
    def __init__(self, engine):
        if not engine:
            raise ValueError("WRONG DB")
        self.engine = engine
        db_engine = create_engine(engine)
        db_session = sessionmaker(bind=db_engine)
	self.session = db_session()
	
    def init_database(self):
        init_database(self.engine)
        
        
    '''STORIES'''  
    def add_story(self, title, content):
        #owner id will be the current user
         new_story = Story(title = title,
                            isTrending = False,
                            number_of_additions = 0,
                            number_of_bookmarks = 0,
                            unique_indicies_count = 1,
                            owner_id = 1321,
                            genre_id = 1332)
         self.session.add(new_story)
         self.session.commit()
        #need to save this object before I make the id availible
         new_story_base = Addition(content = content,
                                    indexReference = 0,
                                    book_marks = 0,
                                    owner_id = 1201302,
                                    story_id = new_story.id,
                                    is_base = True
                                    )
                                    
         
                                    
         self.session.add(new_story_base)
         self.session.commit()
         return new_story
         
    def get_story(self, id, serialize=True):
        storyQuery = self.session.query(Story).get(id)
        all_additions = []  
        for addition in storyQuery.additions.all():
            all_additions.append(self.default_parser(addition))
            if addition.is_base == True:
                base = self.default_parser(addition)
        if serialize:
            return {"story": storyQuery.to_json(base, all_additions)}
            
    def get_stories(self, serialize=True):
        #this will not return their bases/additions
        all_stories = self.session.query(Story).order_by(Story.title).all()
        if serialize:
            return [story.to_json() for story in all_stories]
            
    def get_stories_for_genre(self, genreid, serialize=True):
        all_stories = self.session.query(Story).filter(Story.genre_id == id).all()
        if serialize:
            return [story.to_feed_json() for story in all_stories]
    #this will just get all of the trending stories
    #there needs to be a mechanism that makes them trending...
    #TRENDING WILL BE A RECOMMENDATION SERVICE
    def get_trending_stories(self, serialize=True):
        trending_stories = self.session.query(Story).filter(Story.is_trending == True).all()
        
    '''ADDITIONS'''
    
    def get_all_additions(self, serialize=True):
        all_additions = self.session.query(Addition).orderby
    
    def add_new_addition(self, storyid, content, indexRef):
        
        if storyid is None:
            return {}
        
        new_addition = Addition(content = content,
                                indexReference = indexRef,
                                book_marks = 0,
                                owner_id = 1201302,
                                story_id = storyid,
                                is_base = False)
        self.session.add(new_addition)
        self.session.commit()
        return new_addition
        
    def get_additions_for_story(self, storyId,serialize=True):
        all_additions = self.session.query(Addition).filter(Addition.story_id == id).all()
        if serialize:
            return [add.to_json() for add in all_additions]
            
    
    '''GENRES'''
    def add_genres(self):
        all_genres = self.create_all_base_genres()
        if all_genres is not None:
            return {"Success": "Base Genres have been created"}
    
    def get_genres(self, serialize=True):
        all_genres = self.session.query(Genre).order_by(Genre.title).all()
        if serialize:
            return [genre.to_json() for genre in all_genres]

    '''HELPER STUFF'''  
    def default_parser(self, o):
        if isinstance(o, tuple):
            data = {}
            for obj in o:
                data.update(self.parse_sqlalchemy_object(obj))
            return data
        if isinstance(o.__class__, DeclarativeMeta):
            return self.parse_sqlalchemy_object(o)
        return json.JSONEncoder.default(self,o)
        
    def parse_sqlalchemy_object(self, o):
        data = {}
        fields = o.to_json() if hasattr(o, 'to_json') else dir(o)
        for field in [f for f in fields if not f.startswith('_') and f not in ['metadata', 'query', 'query_class']]:
            value = o.__getattribute__(field)
            try:
                json.dumps(value)
                data[field] = value
            except TypeError:
                data[field] = None
        return data
        
    def mark_online(self, user_id):
        now = int(time.time())
        expires = now + (app.config['ONLINE_LAST_MINUTES'] * 60) + 10
        all_users_key = 'online-users/%d' % (now // 60)
        user_key = 'user-activity/%s' % user_id
        #return a pipline object that can queue multiple commands for later execution
        p = redis.pipeline()
        #add values to set
        p.sadd(all_users_key, user_id)
        p.set(user_key, now)
        #set expire flag on key
        p.expireat(all_users_key, expires)
        p.expireat(user_key, expires)
        p.execute()
        
    def get_user_last_activity(user_id):
        last_active = redis.get('user-activity/%s' % user_id)
        if last_active is None:
            return None
        return datetime.utcfromtimestamp(int(last_active))
        
    def get_online_users():
        current = int(time.time()) // 60
        minutes = xrange(app.config['ONLINE_LAST_MINUTES'])
        return redis.sunion(['online-users/%d' % (current - x) for x in minutes])
        
    def create_all_base_genres(self):
        action_genre = Genre(title="Action", description="Everything Action! From Heroes to Villians. Cars to Explosions. Get your high octane fix.")
        self.session.add(action_genre)
        self.session.commit()
        
        adventure_genre = Genre(title="Adventure", description="Discover all new journeys when venturing into the realm of Adventure!")
        self.session.add(adventure_genre)
        self.session.commit()
        
        comedy_genre = Genre(title="Comedy", description="Laughs and outragious stories await you while reading into the world of Comedy.")
        self.session.add(comedy_genre)
        self.session.commit()
        
        drama_genre = Genre(title="Drama", description="Drama starts, but where does it end?")
        self.session.add(drama_genre)
        self.session.commit()
        
        fantasy_genre = Genre(title="Fantasy", description="Dragons, Knights, and Goblins.")
        self.session.add(fantasy_genre)
        self.session.commit()
        
        horror_genre = Genre(title="Horror", description="No one is safe..")
        self.session.add(horror_genre)
        self.session.commit()
        
        mystery_genre = Genre(title="Mystery", description="Discover what secrets lay within.")
        self.session.add(mystery_genre)
        self.session.commit()
        
        romance_genre = Genre(title="Romance", description="Love is in the air.")
        self.session.add(romance_genre)
        self.session.commit()
        
    
        
        
    
    '''@app.before_request
    def mark_current_user_online(self, user_id):
        self.mark_online(user_id)
        '''    