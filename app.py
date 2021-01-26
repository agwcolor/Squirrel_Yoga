import sys
import os
from flask import Flask, request, abort, flash, json, jsonify, render_template, redirect, url_for
from models import setup_db, db, Person, Teacher, Course, Tree, Event
#import config
from flask_cors import CORS
import dateutil.parser
import babel
from flask_wtf import FlaskForm
from forms import *
from datetime import datetime


def create_app(test_config=None):

    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    setup_db(app)
    print("nothings working")
    CORS(app)
    return app


app = create_app()


# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


'''def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime'''

# ----------------------------------------------------------------------------#
#  Controllers.
# ----------------------------------------------------------------------------#


@app.route('/')
@app.route('/index')
@app.route('/index.html')

def get_greeting():
    excited = os.environ['EXCITED']
    greeting = "Squirrel Yoga"
    if excited == 'true':
        greeting += "!!!!!"
    #return greeting
    return render_template('index.html', greeting=greeting, excited=excited)


@app.route('/coolsquirrel')
def be_cool():
    return render_template('index.html', greeting="Be cool man", excited="I'd rather be surfing")
    #return "Be cool, man, go gather more nuts!"


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
                "moves": teacher.moves,
                "img_url": teacher.img_url
            })
        print(data)
        '''
        return jsonify({
            'success': True,
            'count': len(teachers),
            'data': data
        })
        '''
        return render_template('teachers.html', teachers=data)
    except Exception:
        abort(422)


@app.route('/teachers/<int:id>', methods=['GET'])
def show_teacher(id):

    teacher = Teacher.query.filter(Teacher.id == id).one_or_none()
    if teacher:
        try:
            data = []
            u_events = db.session.query(Event).filter(Event.teacher_id == id).filter(
                Event.course_date > datetime.now()).all()
            print("  my ", len(u_events), " upcoming events", u_events)

            p_events = db.session.query(Event).filter(Event.teacher_id == id).filter(
                Event.course_date < datetime.now()).all()
            print("  my ", len(p_events), " past events", p_events)
            

            upcoming_events = []
            for event in u_events:
                print(event, " is the event")
                course = db.session.query(Course).filter(Course.id==event.course_id).all()
                tree = db.session.query(Tree).filter(Tree.id==event.tree_id).all()
                if len(course) > 0:
                    upcoming_events.append({
                        "course_id": course[0].id,
                        "course_name": course[0].name,
                        "course_date": event.course_date,
                        "tree_name": tree[0].name,
                        "tree_type": tree[0].type,
                        "tree_location": tree[0].location,
                        "tree_img_url": tree[0].img_url
                    })

            past_events = []
            for event in p_events:
                print(event, " is the event")

                course = db.session.query(Course).filter(
                    event.course_id == Course.id).all()
                tree = db.session.query(Tree).filter(Tree.id==event.tree_id).all()

                if len(course) > 0:
                    past_events.append({
                        "course_id": course[0].id,
                        "course_name": course[0].name,
                        "course_date": event.course_date,
                        "tree_name": tree[0].name,
                        "tree_type": tree[0].type,
                        "tree_location": tree[0].location,
                        "tree_img_url": tree[0].img_url
                    })
            #print("upcoming events, past events", upcoming_events, past_events)
            data.append({
                "id": teacher.id,
                "age": teacher.age,
                "name": teacher.name,
                "temperament": teacher.temperament,
                "moves": teacher.moves,
                "img_url": teacher.img_url,
                "upcoming_events": upcoming_events,
                "past_events": past_events,
                "past_events_count": len(db.session.query(Event).filter(Event.teacher_id == teacher.id).filter(Event.course_date < datetime.now()).all()),
                "upcoming_events_count": len(db.session.query(Event).filter(Event.teacher_id == teacher.id).filter(Event.course_date > datetime.now()).all())
            })


            print(data, "is the data")
            print(type(data[0]))
            return render_template('show_teacher.html', teacher=data[0])

            #print(data[0].temperament, " is the temperament")

        except Exception as e:
            exception_type, exception_object, exception_traceback = sys.exc_info()

            filename = exception_traceback.tb_frame.f_code.co_filename

            line_number = exception_traceback.tb_lineno

            print("Exception type: ", exception_type)
            print("File name: ", filename)
            print("Line number: ", line_number)
            print(e, " is the error")
            abort(422)
    else:
        abort(404)


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
        new_img = body.get('image_url', None)
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

@app.route('/teachers/<int:id>/edit', methods=['GET'])
def retrieve_teacher_info(id):
    teacher = Teacher.query.filter(Teacher.id == id).one_or_none()
    form = TeacherForm(obj=teacher)  # Populate form with teacher
    return render_template('forms/edit_teacher.html', form=form, teacher=teacher)


@app.route('/teachers/<int:id>/edit',
           methods=['POST'])  # plural collection endpoint
def edit_teacher(id):
    teacher = Teacher.query.filter(Teacher.id == id).one_or_none()
    form = TeacherForm(request.form)
    if teacher:
        try:
            teacher.name = form.name.data
            teacher.age = form.age.data
            teacher.temperament = form.temperament.data
            teacher.moves = form.moves.data
            teacher.img_url = form.img_url.data
            db.session.commit()
            teacher_id = teacher.id
            
            flash('Teacher ' + teacher.name + ' was just updated!')
            '''return jsonify({
                "success": True,
                "modidifed": teacher_id,
                "name": teacher.name,
                "moves": teacher.moves
            })'''
            return redirect(url_for('show_teacher', id=teacher_id))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Teacher could not be listed.')
            print(e)
            abort(422)
        finally:
            db.session.close()
    else:
        abort(404)

@app.route('/teachers/<int:id>', methods=['DELETE'])
#@requires_auth('delete:drinks')
def delete_teacher(id):
    teacher = Teacher.query.filter(Teacher.id == id).one_or_none()

    if teacher:
        try:
            teacher_id = teacher.id
            db.session.delete(teacher)
            db.session.commit()
            return jsonify({
                "success": True,
                "delete": teacher_id
            })
        except Exception as e:
            db.session.rollback()
            print(e)
            abort(422)
        finally:
            db.session.close()
    else:
        abort(404)


@app.route('/courses', methods=['GET'])
def get_courses():
    try:
        courses = Course.query.order_by(Course.id).all()
        data = []
        for course in courses:
            event_courses = db.session.query(Event).filter(Event.course_id == course.id).all()
            course_teachers = []
            for e in event_courses:
                print(e.teacher_id, "is the teacher id")
            #print(event_courses, "are the courses")
                teacher = db.session.query(Teacher).filter(Teacher.id == e.teacher_id).all()[0]
                print(teacher.name, "whaddaya")
                course_teachers.append({
                        "teacher_name": teacher.name,
                        "teacher_id": teacher.id
                })

            data.append({
                "id": course.id,
                "name": course.name,
                "course_teachers": course_teachers,
                "course_level": course.course_level
                
            })
        print(data, " is the data")
        '''
        return jsonify({
            'success': True,
            'count': len(courses),
            
            'data': data
        })
        '''
        return render_template('courses.html', courses=data)
    except Exception:
        abort(422)


@app.route('/courses/<int:id>', methods=['GET'])
def show_course(id):

    course = Course.query.filter(Course.id == id).one_or_none()
    if course:
        try:
            data = []
            u_events = db.session.query(Event).filter(Event.course_id == id).filter(
                Event.course_date > datetime.now()).all()
            print("  my ", len(u_events), " upcoming events", u_events)

            p_events = db.session.query(Event).filter(Event.course_id == id).filter(
                Event.course_date < datetime.now()).all()
            print("  my ", len(p_events), " past events", p_events)
            

            upcoming_events = []
            for event in u_events:
                print(event, " is the event")
                teacher = db.session.query(Teacher).filter(Teacher.id==event.teacher_id).all()
                tree = db.session.query(Tree).filter(Tree.id==event.tree_id).all()
                if len(teacher) > 0:
                    upcoming_events.append({
                        "teacher_id": teacher[0].id,
                        "teacher_name": teacher[0].name,
                        "course_date": event.course_date,
                        "tree_name": tree[0].name,
                        "tree_type": tree[0].type,
                        "tree_location": tree[0].location,
                        "tree_img_url": tree[0].img_url
                    })

            past_events = []
            for event in p_events:
                print(event, " is the event")
                teacher = db.session.query(Teacher).filter(Teacher.id==event.teacher_id).all()
                tree = db.session.query(Tree).filter(Tree.id==event.tree_id).all()
                if len(teacher) > 0:
                    past_events.append({
                        "teacher_id": teacher[0].id,
                        "teacher_name": teacher[0].name,
                        "course_date": event.course_date,
                        "tree_name": tree[0].name,
                        "tree_type": tree[0].type,
                        "tree_location": tree[0].location,
                        "tree_img_url": tree[0].img_url
                    })
            #print("upcoming events, past events", upcoming_events, past_events)
            data.append({
                "id": course.id,
                "name": course.name,
                "course_level": course.course_level,
                "upcoming_events": upcoming_events,
                "past_events": past_events,
                "past_events_count": len(db.session.query(Event).filter(Event.course_id == course.id).filter(Event.course_date < datetime.now()).all()),
                "upcoming_events_count": len(db.session.query(Event).filter(Event.course_id == course.id).filter(Event.course_date > datetime.now()).all())
            })


            print(data, "is the data")
            print(type(data[0]))
            return render_template('show_course.html', course=data[0])

            #print(data[0].temperament, " is the temperament")

        except Exception as e:
            exception_type, exception_object, exception_traceback = sys.exc_info()

            filename = exception_traceback.tb_frame.f_code.co_filename

            line_number = exception_traceback.tb_lineno

            print("Exception type: ", exception_type)
            print("File name: ", filename)
            print("Line number: ", line_number)
            print(e, " is the error")
            abort(422)
    else:
        abort(404)






'''
Endpoint : POST a new yoga course,
Requires: Course name text, level number.
TEST:

curl http://127.0.0.1:5000/courses/add
-X POST
-H "Content-Type: application/json"
-d '{"name":"Dangle","course_level":5}'

'''


@app.route('/courses/add',
           methods=['POST'])  # plural collection endpoint
def create_course():
    try:
        body = request.get_json()
        new_course = body.get('name', None)
        new_level = body.get('course_level', None)
        course = (
            Course(
                name=new_course,
                course_level=new_level,
                )
            )
        db.session.add(course)  # course.insert()
        db.session.commit()
        course_id = course.id
        flash('Course ' + new_course + ' was just added!')
        return jsonify({
            "success": True,
            "created": course_id
        })
    except Exception as e:
        db.session.rollback()
        flash('An error occurred. Course could not be listed.')
        print(e)
        abort(422)
    finally:
        db.session.close()

@app.route('/courses/<int:id>/edit',
           methods=['GET'])  # plural collection endpoint
def retrieve_course_info(id):
    course = Course.query.filter(Course.id == id).one_or_none()
    form = CourseForm(obj=course)  # Populate form with course
    return render_template('forms/edit_course.html', form=form, course=course)


@app.route('/courses/<int:id>/edit',
           methods=['POST'])  # plural collection endpoint
def edit_course(id):
    course = Course.query.filter(Course.id == id).one_or_none()
    form = CourseForm(obj=course)  # Populate form with course

    if course:
        try:
            course.name = form.name.data
            course.course_level = form.course_level.data
            db.session.commit()
            course_id = course.id
            flash('Course ' + course.name + ' was just updated!')
            '''return jsonify({
                "success": True,
                "modidifed": course_id,
                "name": course.name,
                "level": course.course_level
            })'''
            return redirect(url_for('show_course', id=course_id))

        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Course could not be listed.')
            print(e)
            abort(422)
        finally:
            db.session.close()
    else:
        abort(404)

@app.route('/courses/<int:id>', methods=['DELETE'])
#@requires_auth('delete:drinks')
def delete_course(id):
    course = Course.query.filter(Course.id == id).one_or_none()
    print(course, " is the course")
    if course:
        try:
            course_id = course.id
            db.session.delete(course)
            db.session.commit()
            return jsonify({
                "success": True,
                "delete": course_id
            })
        except Exception as e:
            db.session.rollback()
            print(e)
            abort(422)
        finally:
            db.session.close()
    else:
        abort(404)


if __name__ == '__main__':
    app.run()


@app.route('/trees', methods=['GET'])
def get_trees():
    try:
        trees = Tree.query.order_by(Tree.id).all()
        data = []
        for tree in trees:
            data.append({
                "id": tree.id,
                "name": tree.name,
                "tree_type": tree.type,
                "tree_location": tree.location,
                "img_url": tree.img_url
            })
        print(data)
        return jsonify({
            'success': True,
            'count': len(trees),
            'data': data
        })
    except Exception:
        abort(422)

@app.route('/events')
def get_events():
    events = db.session.query(Event).all()
    data = []
    for event in events:
        teacher_name = db.session.query(Teacher).filter(
            event.teacher_id == Teacher.id).all()[0].name
        course_name = db.session.query(Course).filter(
            event.course_id == Course.id).all()[0].name
        tree_name = db.session.query(Tree).filter(
            event.tree_id == Tree.id).all()[0].name
        '''teacher_image_link = db.session.query(Teacher).filter(
            event.teacher_id == Teacher.id).all()[0].image_link'''
        data.append({
            "course_id": event.course_id,
            "teacher_id": event.teacher_id,
            "course_date": event.course_date,
            "teacher_name": teacher_name,
            "tree_name": tree_name,
            "course_name": course_name,
            #"teacher_image_link": teacher_image_link
        })

    return render_template('events.html', events=data)
