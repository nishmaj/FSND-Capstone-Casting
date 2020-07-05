# FSND Casting Agency Capstone project

## capstone project for the udacity full stack nanodegree program.

**Heroku link:** (https://fsnd-cap-casting.herokuapp.com//)

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in api.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Running the server

To run the server, execute:

```
export FLASK_APP=app.py
export FLASK_ENV=debug
flask run --reload
```


## Casting Agency Specifications

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Models

Movies with attributes contain title, release date, year and director 
Actors with attributes name, age, role and gender

## Environment Variables

In the `.env` file, the JWT token for each User Role
- CASTING_ASSISTANT
- CASTING_DIRECTOR
- EXECUTIVE_PRODUCER

## Roles

Casting Assistant
##### All permissions a Casting Assistant has
- GET:actors
- GET:movies

Casting Director
#####  All permissions a Casting Director has
- POST:actor
- DELETE:actor
- PATCH:actor
- PATCH:movie

Executive Producer

##### All permissions an Executive Producer has
- POST:movie
- DELETE:movie

## Endpoints

`````bash
GET '/actors'

response =
{
  "actors": [
    {
      "age": 40,
      "gender": "M",
      "id": 1,
      "movie_id": 1,
      "name": "Tom Hanks",
      "role": "Tiger"
    }
  ],
  "success": true
}


POST '/actors/add'

response = {
  "created": 1,
  "new_actor": {
    "age": 40,
    "gender": "M",
    "id": 1,
    "movie_id": 1,
    "name": "Tom Hanks",
    "role": "Tiger"
  },
  "success": true
}

PATCH '/actors/update/<int:actor_id>'

params = <int:actor_id>

response = {
  "actor": {
    "age": 30,
    "gender": "F",
    "id": 2,
    "movie_id": 1,
    "name": "Tom Cruise",
    "role": "Mav"
  },
  "message": "Actor has been updated",
  "success": true
}

DELETE '/actors/delete/<int:actor_id>'

params = <int:actor_id>

response = {
  "message": "Actor has been deleted",
  "success": true
}

GET '/movies'

response = {
  "movies": [
    {
      "actors": [
        {
          "age": 40,
          "gender": "M",
          "id": 1,
          "movie_id": 1,
          "name": "Tom Hanks",
          "role": "Tiger"
        }
      ],
      "director": "David Fagan",
      "id": 1,
      "release_date": "Wed, 01 Apr 2020 00:00:00 GMT",
      "title": "Jurasic park",
      "year": 2005
    }
  ],
  "success": true
}

POST '/movies/add'

response = {
  "created": 1,
  "new_movie": {
    "actors": [],
    "director": "David Fagan",
    "id": 1,
    "release_date": "Wed, 01 Apr 2020 00:00:00 GMT",
    "title": "Jurasic park",
    "year": 2005
  },
  "success": true
}

PATCH '/movies/update/<int:movie_id>'

params = <int:movie_id>

response = {
  "message": "Movie has been updated",
  "movie": {
    "actors": [
      {
        "age": 40,
        "gender": "M",
        "id": 1,
        "movie_id": 1,
        "name": "Tom Hanks",
        "role": "Tiger"
      }
    ],
    "director": "David Fagan",
    "id": 1,
    "release_date": "Wed, 01 Apr 2020 00:00:00 GMT",
    "title": "Jurasic park 2",
    "year": 2010
  },
  "success": true
}


DELETE '/movies/delete/<int:movie_id>'
params = <int:movie_id>

response = {
  "message": "Movie has been deleted",
  "success": true
}

`````
## Testing

To run the tests, and run in your terminal

```bash

python test_app.py
`````