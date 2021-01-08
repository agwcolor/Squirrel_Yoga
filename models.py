from sqlalchemy import Column, String, Integer, DateTime, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os

#----------------------------------------------------------------------------#
#  App Config.
#----------------------------------------------------------------------------#

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()
# migrate = Migrate(app, db, compare_type=True)  -- what does this do
'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    #db.create_all()


#----------------------------------------------------------------------------#
# Models
#----------------------------------------------------------------------------#


'''
Person
Have title and release year
'''
class Person(db.Model):  
  __tablename__ = 'People'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  catchphrase = Column(String)

  def __init__(self, name, catchphrase=""):
    self.name = name
    self.catchphrase = catchphrase

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'catchphrase': self.catchphrase}

class Actor(db.Model):
  __tablename__ = 'Actor'

  id = Column(Integer, primary_key=True)
  name = Column(String)
  age = Column(Integer)
  gender = Column(String)
  movies = db.relationship('Movie', backref='Actor', lazy=True)

  '''def __init__(self, name, catchphrase=""):
    self.name = name
    self.catchphrase = catchphrase'''

  def format(self):
    return {
      'id': self.id,
      'name': self.name,
      'gender': self.gender}

  def __repr__(self):
    return f'<Actor ID: {self.id}, name: {self.name}, gender: {self.gender}>'

class Movie(db.Model):
  __tablename__ = 'Movie'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  release_date = Column(DateTime)
  artist_id = Column(Integer, db.ForeignKey('Actor.id'))


  '''def __init__(self, name, catchphrase=""):
    self.name = name
    self.catchphrase = catchphrase'''

  def format(self):
    return {
      'id': self.id,
      'title': self.name,
      'release_date': self.release_date}
  
  def __repr__(self):
    return f'<Movie ID: {self.id}, title: {self.name}, release_date: {self.release_date}>'