from sqlalchemy import Column, String, Integer, DateTime, create_engine
from sqlalchemy.dialects.postgresql import ARRAY
from flask_sqlalchemy import SQLAlchemy
import json
import os

# ----------------------------------------------------------------------------#
#  App Config.
# ----------------------------------------------------------------------------#

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
    print("Did this do anything?")


# ----------------------------------------------------------------------------#
# Models
# ----------------------------------------------------------------------------#


'''
Person
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


class Teacher(db.Model):
    __tablename__ = 'Teacher'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    temperament = Column(String)
    moves = Column(ARRAY(String))
    events = db.relationship("Event", cascade="all, delete", backref="Teacher", lazy=True)


    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'temperament': self.temperament,
            'moves': self.moves}

    def __repr__(self):
        return f'<Teacher ID: {self.id}, name: {self.name}, age: {self.age}, \
      temperament: {self.temperament}, moves: {self.moves}>'


class Course(db.Model):
    __tablename__ = 'Course'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    course_level = Column(Integer)
    events = db.relationship("Event", backref="Course", lazy=True)

    def format(self):
        return {
            'id': self.id,
            'title': self.name,
            }

    def __repr__(self):
        return f'<Course ID: {self.id}, title: {self.name}, course_level: {self.course_level}>'


class Event(db.Model):
    __tablename__ = 'Event'

    id = Column(Integer, primary_key=True)
    tree = Column(String)
    course_date = Column(DateTime)
    teacher_id = Column(Integer, db.ForeignKey('Teacher.id'), nullable=False)
    course_id = Column(Integer, db.ForeignKey('Course.id'), nullable=False)

    def format(self):
        return {
            'id': self.id,
            'tree': self.tree,
            'course_date': self.course_date}

    def __repr__(self):
        return f'<Course ID: {self.id}, tree: {self.tree}, course_date: \
      {self.course_date}>'
