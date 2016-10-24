#This will be the story controller - deals with everything for a story
#do i want blueprints? 
from flask import Blueprint, request, g, session, redirect, url_for
from app import db

#import module models
from app.models import Story, Addition

#define the blueprint: 'story' - set the url prefix to story
mod_story = Blueprint('story', __name__, url_prefix = '/story')

'''the purpose of these controllers is to just return json that I want

    NOTE: not all the functions in here have to be routes
''' 

#set route and accepted methods
@mod_story.route('/active_additions/', methods=['GET'])
def get_active_additions_for_story(storyid):
    pass
    
def get_story_bookmarks_count():
    pass
    
def get_story_base(storyid):
    pass
 
#when getting a story, you must also get all its additions and its base   
@mod_story.route('/<int:storyid>/', methods=['GET'])
def get_story(storyid):
    story = Story.query.filter(Story.id=storyid)
    all_additions = story.additions.all()
    for addition in all_additions:
        if addition.index_reference is None:
            base = addition
    
@mod_story.route('', methods=['POST'])
def add_story():
    pass
    
    
    
    '''CHECKING TO SEE HOW YOU GET RELATIONSHIPS TO JSON -> you can use session through db.session!!!'''
    #LOOK INTO HOW TO STRUCTURE THIS BETTER!!!
    