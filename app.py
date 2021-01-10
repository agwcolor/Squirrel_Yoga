import os
from flask import Flask, request, abort, flash, json, jsonify
from models import setup_db, db, Teacher, Course
import config
from flask_cors import CORS
import dateutil.parser
import babel


def create_app(test_config=None):

    app = Flask(__name__)
    app.secret_key = os.urandom(24)
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


'''
Endpoint : POST a new teacher,
Requires: teacher name text, age number, temperament, and moves.
TEST:

curl http://127.0.0.1:5000/teachers/add
-X POST
-H "Content-Type: application/json"
-d '{"name":"Reuil1","age":5, "temperament":"frisky",
    "moves":"my fav move"}'

'''


@app.route('/teachers/add',
           methods=['POST'])  # plural collection endpoint
def create_teacher():
    try:
        body = request.get_json()
        new_teacher = body.get('name', None)
        new_age = body.get('age', None)
        new_temperament = body.get('temperament', None)
        new_moves = body.get('moves', None)
        teacher = (
            Teacher(
                name=new_teacher,
                age=new_age,
                temperament=new_temperament,
                moves=new_moves)
            )
        db.session.add(teacher)  # teacher.insert()
        db.session.commit()
        teacher_id = teacher.id
        flash('Teacher ' + new_teacher + ' was just added!')
        return jsonify({
            "success": True,
            "created": teacher.id
        })
    except Exception as e:
        db.session.rollback()
        flash('An error occurred. Teacher' + new_teacher + ' could not be listed.')
        print(e)
        abort(422)
    finally:
        db.session.close()


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
