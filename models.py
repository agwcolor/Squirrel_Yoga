from sqlalchemy import Column, String, Integer, DateTime, create_engine
from sqlalchemy.dialects.postgresql import ARRAY
from flask_sqlalchemy import SQLAlchemy
import os


# ----------------------------------------------------------------------------#
#  App Config.
# ----------------------------------------------------------------------------#

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()
# migrate = Migrate(app, db, compare_type=True)
'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # db.create_all()

# ----------------------------------------------------------------------------#
# Models
# ----------------------------------------------------------------------------#


class Teacher(db.Model):
    __tablename__ = 'Teacher'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    temperament = Column(String)
    moves = Column(ARRAY(String))
    img_url = Column(String)
    events = db.relationship(
        "Event",
        cascade="all, delete",
        backref="Teacher",
        lazy=True)

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
        return f'<Course ID: {self.id}, title: {self.name}, \
            course_level: {self.course_level}>'


class Event(db.Model):
    __tablename__ = 'Event'

    id = Column(Integer, primary_key=True)
    course_date = Column(DateTime)
    teacher_id = Column(Integer, db.ForeignKey('Teacher.id'), nullable=False)
    course_id = Column(Integer, db.ForeignKey('Course.id'), nullable=False)
    tree_id = Column(Integer, db.ForeignKey('Tree.id'), nullable=True)

    def format(self):
        return {
            'id': self.id,
            'course_date': self.course_date}

    def __repr__(self):
        return f'<Course ID: {self.id}, course_date:{self.course_date}>'


class Tree(db.Model):
    __tablename__ = 'Tree'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    location = Column(String)
    img_url = Column(String)
    events = db.relationship("Event", backref="Tree", lazy=True)

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'location': self.location
        }

    def __repr__(self):
        return f'<Tree ID: {self.id}, name: {self.name}, type: {self.type}, \
            location: {self.location}>'
