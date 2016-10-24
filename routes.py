##API ROUTES

from flask import jsonify
from flask import render_template
from flask import flash
from flask import current_app
from flask import abort

from Middleware import create_story
from Middleware import add_genres
from Middleware import get_story_by_id
from Middleware import initialize_database as init_db
from Middleware import build_message

def init_api_routes(app):
    if app:
        app.add_url_rule('/api/stories', 'add_story', create_story, methods=["POST"])
        app.add_url_rule('/api/stories/<string:id>', 'get_story_by_id', get_story_by_id, methods=["GET"])
        app.add_url_rule('/api/genres', 'add_genres', add_genres, methods=["GET"])
        
def crash_server():
    abort(500)
    
def initialize_database():
    message_key = "Init DB"
    try:
        init_db()
    except ValueError as err:
        return jsonify(build_message(message_key, err.message))
    return jsonify(build_message(message_key, "Success")) 

'''
api.add_url_rule('/api/story/<string:id>', 'story_by_id', story_by_id, methods=["GET"])
api.add_url_rule('/api/stories', 'stories', get_all_stories, methods=["GET"])
api.add_url_rule('/api/stories', 'add_story', create_story, methods=["POST"])
api.add_url_rule('/api/stories/<string:id>', 'update_story', update_story, methods=["PUT"])
api.add_url_rule('/api/stories/random', 'get_one_random_story', random_stories, methods=["GET"], defaults={'nr_of_items':1})
api.add_url_rule('/api/stories/random/<int:nr_of_items>', 'get_random_stories', random_stories, methods=['GET'])
api.add_url_rule('/api/stories/delete/<string:id>', 'delete_story', delete_story, methods=["DELETE"])




api.add_url_rule('/api/initdb', 'initdb', initialize_database)
'''