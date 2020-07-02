import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db_drop_and_create_all, setup_db, Movie, Actor, db


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  #db_drop_and_create_all()

  @app.after_request
  def after_request(response):
      header = response.headers
      header['Access-Control-Allow-Origin'] = '*'
      header['Access-Control-Allow-Headers'] = 'Authorization, Content-Type, true'
      header['Access-Control-Allow-Methods'] = 'POST,GET,PUT,DELETE,PATCH,OPTIONS'
      return response


  ## ROUTES
 
  @app.route('/')
  def get_index():
      return jsonify('Success')

  '''
  GET /movies
      Public route for getting all movies
      returns status code 200 and json {"success": True, "movies": movies} where movies is the list of movies
          or appropriate status code indicating reason for failure
  '''
  @app.route('/movies', methods=['GET'])
  #@requires_auth('view:movies')
  def get_movies():
      movies = Movie.query.all()
      movies = [movie.format() for movie in movies]
      #print(movies)
      for movie in movies:
        movie['actors'] = [i.format() for i in movie['actors']]
      result = {
        "success": True,
        "movies": movies
      }
      return jsonify(result)

  '''
  GET /actors
      Public route for getting all actors
      returns status code 200 and json {"success": True, "actors": actors} where actors is the list of actors
          or appropriate status code indicating reason for failure
  '''
  @app.route('/actors', methods=['GET'])
  #@requires_auth('view:actors')
  def get_actors():
      actors = Actor.query.all()
      if len(actors) == 0:
            abort(404)
      try:
          actors = [actor.format() for actor in actors]

          return jsonify({
              'success': True,
              'actors': actors,
          }), 200
      except Exception:
          abort(422)


  @app.route('/movies', methods=['POST'])
  #@requires_auth('post:movie')
  def post_new_movie():
      body = request.get_json()

      title = body.get('title', None)
      release_date = body.get('release_date', None)
      year = body.get('year', None)
      director = body.get('director', None)
      movie = Movie(title=title, release_date=release_date,year=year, director=director)
      movie.insert()
      new_movie = Movie.query.get(movie.id)
      new_movie = new_movie.format()

      return jsonify({
        'success': True,
        'created': movie.id,
        'new_movie': new_movie
      })


  @app.route('/actors', methods=['POST'])
  #@requires_auth('post:actor')
  def post_new_actor():
      body = request.get_json()
      name = body.get('name', None)
      age = body.get('age', None)
      gender = body.get('gender', None)
      role = body.get('role', None)
      movie_id = body.get('movie_id', None)

      actor = Actor(name=name, age=age, gender=gender, role=role, movie_id=movie_id)
      actor.insert()
      new_actor = Actor.query.get(actor.id)
      new_actor = new_actor.format()

      return jsonify({
        'success': True,
        'created': actor.id,
        'new_actor': new_actor
      })

  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  #@requires_auth('delete:movie')
  def delete_movie(movie_id):

      # Abort if no movie_id has been provided
      if not movie_id:
        abort(400, {'message': 'please append an movie id to the request url.'})
    
      # Find movie which should be deleted by id
      movie_to_delete = Movie.query.filter(Movie.id == movie_id).one_or_none()

      # If no movie with given id could found, abort 404
      if not movie_to_delete:
          abort(404, {'message': 'Movie with id {} not found in database.'.format(movie_id)})

      movie_to_delete.delete()
      return jsonify({
        "success": True,
        "message" : "Movie has been deleted"
      })

  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  #@requires_auth('delete:actor')
  def delete_actor(actor_id):

      # Abort if no actor_id has been provided
      if not actor_id:
        abort(400, {'message': 'please append an actor id to the request url.'})
    
      # Find actor which should be deleted by id
      actor_to_delete = Actor.query.filter(Actor.id == actor_id).one_or_none()

      # If no actor with given id could found, abort 404
      if not actor_to_delete:
          abort(404, {'message': 'Actor with id {} not found in database.'.format(actor_id)})
      
      # Delete actor from database
      actor_to_delete.delete()
      
      return jsonify({
        "success": True,
        "message" : "Actor has been deleted"
      })

  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  #@requires_auth('patch:movies')
  def patch_movie(movie_id):
      body = request.get_json()

      title = body.get('title', None)
      release_date = body.get('release_date', None)
      year = body.get('year', None)
      director = body.get('director', None)
      movie = Movie.query.filter_by(id=movie_id).one_or_none()

      movie.title = title
      movie.release_date = release_date
      movie.year = year
      movie.director = director

      movie.update()

      movie = movie.format()
      movie['actors'] = [i.format() for i in movie['actors']]

      return jsonify({
        "success": True,
        "message": "Movie has been updated",
        'movie': movie

      })

  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  #@requires_auth('patch:actors')
  def patch_actor(actor_id):
      body = request.get_json()
      print(body) 
      name = body.get('name', None)
      age = body.get('age', None)
      gender = body.get('gender', None)
      role = body.get('role', None)
      movie_id = body.get('movie_id', None)

      actor = Actor.query.filter_by(id=actor_id).one_or_none()
      actor.name = name
      actor.age = age
      actor.gender = gender
      actor.role = role
      actor.movie_id = movie_id

      actor.update()

      return jsonify({
        "success": True,
        "message": "Actor has been updated",
        'actor': actor.format()

      })

  # @app.errorhandler(404)
  # def not_found(error):
  #     return jsonify({
  #       'success': False,
  #       'error' : 404,
  #       'message' : 'Not Found'
  #     }), 404

  # @app.errorhandler(422)
  # def unprocessable_entity(error):
  #     return jsonify({
  #       'success': False,
  #       'error': 422,
  #       'message': 'Unprocessable Entity'
  #     })      

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
                      "success": False, 
                      "error": 422,
                      "message": get_error_message(error,"unprocessable")
                      }), 422

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
                      "success": False, 
                      "error": 400,
                      "message": error_message(error, "bad request")
                      }), 400

  @app.errorhandler(404)
  def ressource_not_found(error):
      return jsonify({
                      "success": False, 
                      "error": 404,
                      "message": error_message(error, "resource not found")
                      }), 404

  # @app.errorhandler(AuthError)
  # def authentification_failed(AuthError): 
  #     return jsonify({
  #                     "success": False, 
  #                     "error": AuthError.status_code,
  #                     "message": AuthError.error['description']
  #                     }), AuthError.status_code


  def error_message(error, default_text):
      try:
          # Return message contained in error, if possible
          return error.description['message']
      except:
          # otherwise, return given default text
          return default_text

  
  return app
app = create_app()

if __name__ == '__main__':
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port, debug=True)