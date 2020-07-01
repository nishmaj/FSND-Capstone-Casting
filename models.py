import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from datetime import date
import json

database_name = 'capstone-casting'
database_path = 'postgres://{}@{}/{}'.format('nishmajain', 'localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''
def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    db_init_records()

def db_init_records():
    '''this will initialize the database with some test records.'''
    new_actor = (Actor(
        name = 'Tom Cruise',
        gender = 'Male',
        age = 30,
        role = 'Tiger',
        movie_id = 1
        ))

    new_movie = (Movie(
        title = 'Topgun',
        release_date = date.today(),
        year = 2000,
        director = 'Jon Hart'
        ))

    # new_actor.insert()
    # new_movie.insert()
    # db.session.commit()

'''
Movie
a persistent movie entity, extends the base SQLAlchemy Model
'''
class Movie(db.Model):

    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    release_date = db.Column(db.Date)
    year = db.Column(db.Integer)
    director = db.Column(db.String)
    actors = db.relationship('Actor', backref='movies')

    '''
    short()
        short form representation of the Movie model
    '''
    def short(self):
        return {
            'id': self.id,
            'title': self.title,
            'year': self.year
        }

    '''
    long()
        long form representation of the Movie model
    '''
    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'year': self.year,
            'director': self.director,
            'actors': json.loads(self.actors)
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
    '''
    def update(self):
        db.session.commit()

    # def format(self):
    #     print(self)s
    #     return {
    #         'id': self.id,
    #         'title': self.title,
    #         'release_date': self.release_date,
    #         'actors': json.loads(self.actors)
    #     }  
    def format(self):
        return{
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'year': self.year,
            'director': self.director,
            'actors': self.actors        
        }
      

    def __repr__(self):
        return json.dumps(self.short())




class Actor(db.Model):
    #this would be the actors table. It will be the child of the Movie table
    __tablename__ = 'actors' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)
    role = db.Column(db.String)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'role' : self.role,
            'movie_id': self.movie_id
        }
    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
  