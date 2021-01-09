import os
from flask import Flask, abort, json, jsonify
from models import setup_db, Teacher, Course
from flask_cors import CORS
import dateutil.parser
import babel


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)
    return app


app = create_app()


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

# ----------------------------------------------------------------------------#
#  Controllers.
# ----------------------------------------------------------------------------#


@app.route('/')
def get_greeting():
    excited = os.environ['EXCITED']
    greeting = "Squirrel Yoga"
    if excited == 'true':
        greeting += "!!!!!"
    return greeting


@app.route('/coolsquirrel')
def be_cool():
    return "Be cool, man, go gather more nuts!"


@app.route('/teachers', methods=['GET'])
def get_teachers():
    try:
        print("I'm in get teachers")
        teachers = Teacher.query.order_by(Teacher.id).all()
        print(len(teachers))
        data = []
        for teacher in teachers:
            data.append({
                "id": teacher.id,
                "age": teacher.age,
                "name": teacher.name,
                "temperament": teacher.temperament,
                "moves": teacher.moves
            })
        print(data)
        return jsonify({
            'success': True,
            'count': len(teachers),
            'data': data
        })
    except Exception:
        abort(422)


@app.route('/courses', methods=['GET'])
def get_courses():
    try:
        courses = Course.query.order_by(Course.id).all()
        data = []
        for course in courses:
            data.append({
                "id": course.id,
                "name": course.name,
                "course_date": course.course_date,
                "course_level": course.course_level
            })
        print(data)
        return jsonify({
            'success': True,
            'count': len(courses),
            'data': data
        })
    except Exception:
        abort(422)


if __name__ == '__main__':
    app.run()
