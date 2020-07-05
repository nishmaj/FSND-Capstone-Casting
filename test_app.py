
import os
import unittest
import json
import logging
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from models import db, Actor, Movie, setup_db, db_drop_and_create_all
from app import create_app
import datetime

class CastingTestCase(unittest.TestCase):

    """This class represents the agency test case"""

    def setUp(self):
        '''define test variables and initialize app'''

        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_URL']

        logging.basicConfig()
        log = logging.getLogger("LOG")

        self.casting_assistant = os.getenv('CASTING_ASSISTANT')
        self.casting_director = os.getenv('CASTING_DIRECTOR')
        self.executive_producer = os.getenv('EXECUTIVE_PRODUCER')

        print(self.casting_assistant)
        setup_db(self.app)
        #db.create_all()
        
        self.new_movie = {
            'title': 'New Test Movie',
            'release_date' : datetime.date(2020, 7, 1),
            'year' : 2000,
            'director' : 'Jon Ross'
        }

        self.new_actor = {
            'name': 'John Doe',
            'age': 22,
            'gender': 'Male',
            'role' : 'Tiger',
            'movie_id': 1
        }

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            #db_drop_and_create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test cases...

    # Test cases for CASTING_ASSISTANT ...
    def test_get_actors_casting_assistant(self):

        res = self.client().get('/actors',
                                headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_assistant)
                                })
        #log = logging.getLogger("LOG")
        #log.warning(self.casting_assistant)

        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_get_movies_casting_assistant(self):

        res = self.client().get('/movies',
                                headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_assistant)
                                })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_add_actor_casting_assistant(self):
        res = self.client().post('/actors/add',
                                 headers={
                                     "Authorization": "Bearer {}".format(
                                         self.casting_assistant)
                                 }, json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        
    def test_add_movie_casting_assistant(self):
        res = self.client().post('/movies/add',
                                 headers={
                                     "Authorization": "Bearer {}".format(
                                         self.casting_assistant)
                                 }, json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)


    # Test cases for export CASTING_DIRECTOR ...
    def test_add_actor_casting_director(self):
        res = self.client().post('/actors/add',
                                 headers={
                                     "Authorization": "Bearer {}".format(
                                         self.casting_director)
                                 }, json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_delete_actor_casting_director(self):
        res = self.client().delete('/actors/delete/1',
                                    headers={
                                     "Authorization": "Bearer {}".format(
                                         self.casting_director)
                                 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_update_actor_casting_director(self):
        res = self.client().patch('/actors/update/1',
                                    headers={
                                     "Authorization": "Bearer {}".format(
                                         self.casting_director)
                                 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_update_movie_casting_director(self):
        res = self.client().patch('/movies/update/1',
                                    headers={
                                     "Authorization": "Bearer {}".format(
                                         self.casting_director)
                                 })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_new_movie_casting_director(self):
        res = self.client().post('/movies/add',
                                    headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_director)
                                    },
                                    json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_delete_movie_casting_director(self):
        res = self.client().delete('/movies/delete/100',
                                    headers={
                                    "Authorization": "Bearer {}".format(
                                        self.casting_director)
                                    })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)


    # Test cases for export EXECUTIVE_PRODUCER ...

    def test_new_movie_executive_producer(self):
        res = self.client().post('/movies/add',
                                    headers={
                                    "Authorization": "Bearer {}".format(
                                        self.executive_producer)
                                    },
                                    json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['new_movie']['title'], 'New Test Movie')

    def test_delete_movie_executive_producer(self):
        res = self.client().delete('/movies/delete/100',
                                    headers={
                                    "Authorization": "Bearer {}".format(
                                        self.executive_producer)
                                    })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)    

\


if __name__ == "__main__":

    # suite = unittest.TestLoader().loadTestsFromTestCase(CastingTestCase)
    # unittest.TestLoader().sortTestMethodsUsing = None
    # testResult = unittest.TextTestRunner(verbosity=4).run(suite)
    # print(testResult)

    unittest.main()
    