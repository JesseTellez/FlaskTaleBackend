from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for

from DataProvider import DataProviderService
db_engine = 'mysql://root:cheeseit007@localhost/taleTestBase'
DATA_PROVIDER = DataProviderService(db_engine)

def initialize_database():
    DATA_PROVIDER.init_database()

'''ADDITION FUNCTIONS'''
def add_addition_to_story(story_id, content, indexRef):
    #I will add logic in here to make sure I can pass this to ML
    content = request.form["content"]
    indexRef = request.form["indexRef"]
    new_addition = DATA_PROVIDER.add_new_addition(id, content, indexRef)
    return jsonify({"addition": new_addition})
    #This doesnt really need to return anything, a new route will be made once this is done saving
    #Once done saving, the app will open a new page causing a new route to fire
    


'''STORY FUNCTIOINS'''

def create_story():
    title = request.form["title"]
    content = request.form["content"]
    new_story = DATA_PROVIDER.add_story(title, content)
    
    #may need to return all the base stuff as an object
    return jsonify({
        "title": new_story.title
    })
    
def get_all_trending_stories():
    trending_stories = DATA_PROVIDER.get_trending_stories(serialize=True)

def get_all_stories_for_genre(id):
    all_specified_stories = DATA_PROVIDER.get_all_stories_for_genre(serialize=True)
    if all_specified_stories:
        return jsonify(stories=all_specified_stories)
    else:
        abort(404)
    
def get_all_stories():
    all_stories = DATA_PROVIDER.get_all_stories(serialize=True)
    if all_stories:
        return jsonify(stories=all_stories)
    else:
        abort(404)

def get_story_by_id(id):
    current_story = DATA_PROVIDER.get_story(id, serialize=True)
    if current_story:
        return jsonify(current_story)
    else:
        abort(404)

'''GENRE FUNCTUIONS'''

def add_genres():
    created_genres = DATA_PROVIDER.add_genres()
    if created_genres:
        return jsonify(created_genres)
    else:
        abort(500)

def get_all_genres(serialize=True):
    all_genres = DATA_PROVIDER.get_genres(serialize=True)
    if all_genres:
        return jsonify(all_genres)
    else:
        abort(500)
    

def build_message(key, message):
    return {key:message}