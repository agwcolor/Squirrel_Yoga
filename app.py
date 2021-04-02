from dotenv import load_dotenv, find_dotenv
import sys
import os
from os.path import join, dirname
from flask import Flask, request, abort, flash, json, jsonify, render_template, redirect, url_for
from models import setup_db, db, Teacher, Course, Tree, Event
# import config
from flask_cors import CORS, cross_origin
import dateutil.parser
import babel
from flask_wtf import FlaskForm
from forms import *
from datetime import datetime
from auth.auth import AuthError, requires_auth, requires_auth_auth0
# from server import AuthError, requires_auth
from authlib.integrations.flask_client import OAuth
from flask import session, g
from six.moves.urllib.parse import urlencode

AUTH0_CALLBACK_URL = os.environ['AUTH0_CALLBACK_URL']
AUTH0_CLIENT_ID = os.environ['AUTH0_CLIENT_ID']
AUTH0_CLIENT_SECRET = os.environ['AUTH0_CLIENT_SECRET']
AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
AUTH0_AUDIENCE = os.environ['AUTH0_AUDIENCE']


def create_app(test_config=None):

    app = Flask(__name__)
    app.secret_key = os.environ['SECRET_KEY']
    setup_db(app)
    print("creating app ...")
    CORS(app)

    @app.after_request  # after request received run this method
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorizatoin')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET,POST,PATCH,DELETE,OPTIONS')
        print(response, " is the response in after_request")
        return response

    oauth = OAuth(app)

    auth0 = oauth.register(
        'auth0',
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        api_base_url=AUTH0_BASE_URL,
        access_token_url=AUTH0_BASE_URL + '/oauth/token',
        authorize_url=AUTH0_BASE_URL + '/authorize',
        client_kwargs={
            'scope': 'openid profile email',
        },
    )


# ----------------------------------------------------------------------------#
# Auth Enpoints.
# ----------------------------------------------------------------------------#

    '''
    @app.route('/logout')
    def logout():
        # Clear session stored data
        session.clear()
        # Redirect user to logout endpoint
        params = {
    'returnTo': url_for(
        'confirm_logout',
        _external=True),
         'client_id': auth0.client_id}
        return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))
    '''
    # Here we're using the /callback route.

    @app.route('/callback')
    @cross_origin()
    def callback_handling():
        # Handles response from token endpoint
        token = auth0.authorize_access_token()
        session['token'] = token['access_token']
        print(session['token'], " is the session token")
        resp = auth0.get('userinfo')
        userinfo = resp.json()

        # Store the user information in flask session.
        session['JWT_PAYLOAD'] = userinfo
        session['profile'] = {
            'user_id': userinfo['sub'],
            'name': userinfo['name'],
            'nickname': userinfo['nickname'],
            'picture': userinfo['picture']
        }
        return redirect('/dashboard', )

    @app.route('/login')
    @cross_origin()
    def login():
        return auth0.authorize_redirect(
            redirect_uri=AUTH0_CALLBACK_URL,
            audience=AUTH0_AUDIENCE)

    @app.route('/logout')
    @cross_origin()
    def logout():
        session.clear()
        params = {
            'returnTo': url_for(
                'confirm_logout',
                _external=True),
            'client_id': AUTH0_CLIENT_ID}
        return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

    @app.route('/confirm-logout', methods=['GET'])
    def confirm_logout():
        return render_template('logged_out.html')

    # /server.py
    '''
    @app.route('/login', methods=['GET'])
    def get_login_page():
        return render_template('home.html')
        '''
    '''
    @app.route('/login-auth')
    def login():
        print('Audience: {}'.format(API_AUDIENCE))
        return auth0.authorize_redirect(
    redirect_uri='http://localhost:5000/callback',
     audience=API_AUDIENCE)
    '''
    ''' AUTH0 Boilerplate '''
    @app.route('/dashboard')
    @cross_origin()
    @requires_auth_auth0()
    def dashboard():
        print(session['profile'], " session profile")
        # print(json.dumps(session['jwt_payload'], " jwt payload"))
        return render_template(
            'dashboard.html',
            userinfo=session['profile'],
            userinfo_pretty=json.dumps(
                session['JWT_PAYLOAD'],
                indent=4))

    # ----------------------------------------------------------------------------#
    #  Controllers.
    # ----------------------------------------------------------------------------#

    @app.route('/', methods=['GET'])
    # @app.route('/index', methods =['GET'])
    # @app.route('/index.html', methods =['GET'])
    @cross_origin()
    def get_home_page():
        if not session:
            print("there is no session")
            userinfo = ""
        elif 'profile' not in session:
            userinfo = ""
            print("there's a session but no profile")
            print(session, " is the session")
        else:
            userinfo = session['profile']
            print(userinfo, "userinfo profile")
        return render_template('index.html', userinfo=userinfo)

    '''@app.route('/coolsquirrel')
    def be_cool():
        return render_template(
    'index.html',
    greeting="Be cool man",
     excited="I'd rather be surfing")
        # return "Be cool, man, go gather more nuts!"
        # '''


#  ----------------------------------------------------------------
#  Teacher Endpoints
#  ----------------------------------------------------------------

    '''
  ENDPOINT: Handles GET requests for teachers,
  Returns: a list of teachers, number of total teachers,
  success true or not.

  TEST: Click the `Teachers` Button to see the list of teachers.

  curl "http://127.0.0.1:5000/teachers

  '''

    @app.route('/teachers', methods=['GET'])
    @cross_origin()
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
            # print(data)

            # return jsonify({
            #     'success': True,
            #     'count': len(teachers),
            #     'data': data
            # })

            return render_template('teachers.html', teachers=data)
        except Exception:
            abort(422)

    '''
    ENDPOINT: Handles GET request for 1 teacher.,
    Returns: teacher details (name,age,temperament,moves) + past and upcoming
        event information

    TEST: Click a teacher name link.

    curl "http://127.0.0.1:5000/teachers/1"

    '''

    @app.route('/teachers/<int:id>', methods=['GET'])
    def show_teacher(id):

        teacher = Teacher.query.filter(Teacher.id == id).one_or_none()
        if teacher:
            try:
                data = []
                u_events = db.session.query(Event).filter(
                    Event.teacher_id == id).filter(
                    Event.course_date > datetime.now()).all()
                print("  my ", len(u_events), " upcoming events", u_events)

                p_events = db.session.query(Event).filter(
                    Event.teacher_id == id).filter(
                    Event.course_date < datetime.now()).all()
                print("  my ", len(p_events), " past events", p_events)

                upcoming_events = []
                for event in u_events:
                    print(event, " is the event")
                    course = db.session.query(Course).filter(
                        Course.id == event.course_id).all()
                    tree = db.session.query(Tree).filter(
                        Tree.id == event.tree_id).all()
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
                    tree = db.session.query(Tree).filter(
                        Tree.id == event.tree_id).all()

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
                # print("upcoming events, past events", upcoming_events,
                # past_events)
                data.append(
                    {
                        "id": teacher.id,
                        "age": teacher.age,
                        "name": teacher.name,
                        "temperament": teacher.temperament,
                        "moves": teacher.moves,
                        "img_url": teacher.img_url,
                        "upcoming_events": upcoming_events,
                        "past_events": past_events,
                        "past_events_count": len(
                            db.session.query(Event).filter(
                                Event.teacher_id == teacher.id).filter(
                                Event.course_date < datetime.now()).all()),
                        "upcoming_events_count": len(
                            db.session.query(Event).filter(
                                Event.teacher_id == teacher.id).filter(
                                Event.course_date > datetime.now()).all())})

                print(data, "is the data")
                print(type(data[0]))
                '''
                return jsonify({
                    "success": True,
                    "data": data
                })
                '''
                return render_template('show_teacher.html', teacher=data[0])

                # print(data[0].temperament, " is the temperament")

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

    ''' Render add a teacher form '''

    @app.route('/teachers/add', methods=['GET'])
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth('post:teachers')
    def retrieve_new_teacher_form(payload):
        form = TeacherForm()
        print("I am here")
        print(form.name.data, "is the data")
        print(form, " is the form")
        return render_template('forms/add_teacher.html', form=form)

    '''
    Endpoint : POST a new teacher,
    Requires: teacher name text, age number, temperament, and moves.
    TEST: Click the Add a teacher button to open the form to add a teacher.

    curl http://127.0.0.1:5000/teachers/add
    -X POST
    -H "Content-Type: application/json"
    -d '{"name":"rocky","age":2, "temperament":"sly", "moves":["outhere","highbounce","horizontal fling"], "img_url":"https://res.cloudinary.com/potatobug/image/upload/c_scale,e_brightness:7,w_180/e_sharpen:100/v1611551627/squirrel_rounded_ey5qgk.jpg"}'

    '''

    @app.route('/teachers/add', methods=['POST'])  # plural collection endpoint
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth('post:teachers')
    def create_teacher(payload):
        form = TeacherForm(request.form)
        print("My form info", type(form), form.name.data)
        if (form.name.data or form.age.data or
                form.temperament.data or form.moves.data or form.img_url.data):
            print("form not valid")

        error = False
        try:
            teacher = Teacher(
                name=form.name.data,
                age=form.age.data,
                temperament=form.temperament.data,
                moves=form.moves.data,
                img_url=form.img_url.data)
            db.session.add(teacher)  # teacher.insert()
            db.session.commit()
            teacher_id = teacher.id

        except Exception as e:
            error = True
            db.session.rollback()
            flash(
                'An error occurred. Teacher' +
                new_teacher +
                ' could not be listed.')
            print(e)
            abort(422)
        finally:
            db.session.close()
        if error:
            flash('Teacher ' + request.form['name'] + ' could not be listed.')
            return render_template('teachers.html')
        else:
            flash('Teacher ' + request.form['name'] + ' was added!')
            return redirect(url_for('show_teacher', id=teacher_id))
            '''
            return jsonify({
                "success": True,
                "created": teacher_id
            })
            '''

    ''' Render edit a teacher form '''

    @app.route('/teachers/<int:id>/edit', methods=['GET'])
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth('patch:teachers')
    def retrieve_teacher_info(payload, id):
        teacher = Teacher.query.filter(Teacher.id == id).one_or_none()
        form = TeacherForm(obj=teacher)  # Populate form with teacher
        return render_template(
            'forms/edit_teacher.html',
            form=form,
            teacher=teacher)

    '''
    Endpoint : PATCH (edit) a teacher,
    Requires: teacher name text, age number, temperament, and moves.
    TEST: Click the Edit a teacher button to open the form to edit a teacher.

    curl http://127.0.0.1:5000/teachers/2/edit
    -X POST
    -H "Content-Type: application/json"
    -d '{"name":"rocky","age":2, "temperament":"sly", "moves":["outhere","highbounce","horizontal fling"], "img_url":"https://res.cloudinary.com/potatobug/image/upload/c_scale,e_brightness:7,w_180/e_sharpen:100/v1611551627/squirrel_rounded_ey5qgk.jpg"}'

    '''

    @app.route('/teachers/<int:id>/edit',
               methods=['PATCH', 'POST'])  # plural collection endpoint
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth('patch:teachers')
    def edit_teacher(payload, id):
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

    '''
    ENDPOINT : DELETE teacher using a teacher ID.
    TEST: Click the Delete button on the individual specific teacher page.
    This should persist in the database & on page refresh.
    curl -X DELETE "http://127.0.0.1:5000/teachers/24"

    '''

    @app.route('/teachers/<int:id>', methods=['POST', 'DELETE'])
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth('delete:teachers')
    def delete_teacher(payload,id):
        teacher = Teacher.query.filter(Teacher.id == id).one_or_none()
        if teacher:
            try:
                # teacher_id = teacher.id
                db.session.delete(teacher)
                db.session.commit()
                '''
                return jsonify({
                    "success": True,
                    "deleted": teacher_id})
                '''
                flash('Teacher ' + teacher.name + ' was successfully deleted!')
                # return render_template('events.html')
                return redirect(url_for('get_teachers'))
            except Exception as e:
                db.session.rollback()
                print(e)
                abort(422)
            finally:
                db.session.close()
        else:
            abort(404)

#  ----------------------------------------------------------------
#  Course Endpoints
#  ----------------------------------------------------------------
    '''
    ENDPOINT: Handles GET requests for courses,
    Returns: a list of courses, number of total courses,
    success true or not.

    TEST: Click the `Courses` Button to see the list of teachers.

    curl "http://127.0.0.1:5000/courses
    '''

    @app.route('/courses', methods=['GET'])
    def get_courses():
        try:
            courses = Course.query.order_by(Course.id).all()
            data = []
            for course in courses:
                event_courses = db.session.query(Event).filter(
                    Event.course_id == course.id).all()
                course_teachers = []
                for e in event_courses:
                    print(e.teacher_id, "is the teacher id")
                    # print(event_courses, "are the courses")
                    teacher = db.session.query(Teacher).filter(
                        Teacher.id == e.teacher_id).all()[0]
                    print(teacher.name, "whaddaya")
                    course_teachers.append({
                        "teacher_name": teacher.name,
                        "teacher_id": teacher.id
                    })

                data.append({
                    "course_id": course.id,
                    "course_name": course.name,
                    "course_teachers": course_teachers,
                    "course_level": course.course_level
                })
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
    
    '''
    ENDPOINT: Handles GET request for 1 course.,
    Returns: course details (name,level) + past and upcoming
        event information

    TEST: Click a course name link.

    curl "http://127.0.0.1:5000/courses/1"

    '''

    @app.route('/courses/<int:id>', methods=['GET'])
    def show_course(id):
        course = Course.query.filter(Course.id == id).one_or_none()
        if course:
            try:
                data = []
                u_events = db.session.query(Event).filter(
                    Event.course_id == id).filter(
                    Event.course_date > datetime.now()).all()
                print("  my ", len(u_events), " upcoming events", u_events)

                p_events = db.session.query(Event).filter(
                    Event.course_id == id).filter(
                    Event.course_date < datetime.now()).all()
                print("  my ", len(p_events), " past events", p_events)

                upcoming_events = []
                for event in u_events:
                    print(event, " is the event")
                    teacher = db.session.query(Teacher).filter(
                        Teacher.id == event.teacher_id).all()
                    tree = db.session.query(Tree).filter(
                        Tree.id == event.tree_id).all()
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
                    teacher = db.session.query(Teacher).filter(
                        Teacher.id == event.teacher_id).all()
                    tree = db.session.query(Tree).filter(
                        Tree.id == event.tree_id).all()
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
                data.append({
                    "id": course.id,
                    "name": course.name,
                    "course_level": course.course_level,
                    "upcoming_events": upcoming_events,
                    "past_events": past_events,
                    "past_events_count": len(p_events),
                    "upcoming_events_count": len(u_events)
                })
                print(data, "is the data")
                print(type(data[0]))
                '''
                return jsonify({
                    "success": True,
                    "data": data
                })
                '''
                return render_template('show_course.html', course=data[0])

                # print(data[0].temperament, " is the temperament")

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

    ''' Render add a course form '''

    @app.route('/courses/add', methods=['GET'])
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth('post:courses')
    def retrieve_new_course_form(payload):
        form = CourseForm()
        print("I am here")
        return render_template('forms/add_course.html', form=form)

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
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth('post:courses')
    def create_course(payload):
        # form = CourseForm(request.form)
        try:
            body = request.form
            print(type(body))
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
            return redirect(url_for('show_course', id=course_id))
            '''
            return jsonify({
                "success": True,
                "created": course_id
            })
            '''
        except Exception as e:
            db.session.rollback()
            flash('An error occurred. Course could not be listed.')
            print(e)
            abort(422)
        finally:
            db.session.close()

    ''' Render edit course form '''

    @app.route('/courses/<int:id>/edit',
               methods=['GET'])  # plural collection endpoint
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth('patch:courses')
    def retrieve_course_info(payload, id):
        course = Course.query.filter(Course.id == id).one_or_none()
        form = CourseForm(obj=course)  # Populate form with course
        return render_template(
            'forms/edit_course.html',
            form=form,
            course=course)

    '''
    Endpoint : PATCH (edit) a course,
    Requires: course name text, course level.
    TEST: Click the Edit a course button to open the form to edit a teacher.

    curl http://127.0.0.1:5000/courses/2/edit
    -X PATCH
    -H "Content-Type: application/json"
    -d '{"name":"stretch","level":2}'

    '''

    @app.route('/courses/<int:id>/edit',
               methods=['POST', 'PATCH'])  # plural collection endpoint
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth('patch:courses')
    def edit_course(payload, id):
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

    '''
    ENDPOINT : DELETE course using a course ID.
    TEST: Click the Delete button on the individual course page.
    This should persist in the database & on page refresh.
    curl -X DELETE "http://127.0.0.1:5000/courses/24"

    '''

    @app.route('/courses/<int:id>', methods=['DELETE', 'POST'])
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth('delete:courses')
    def delete_course(payload, id):
        course = Course.query.filter(Course.id == id).one_or_none()
        course_name = course.name
        print(course, " is the course")
        if course:
            try:
                course_id = course.id
                db.session.delete(course)
                db.session.commit()
                '''
                return jsonify({
                    "success":True,
                    "delete":course_id
                })
                '''
                flash('Course ' + course_name + ' was successfully deleted!')
                return redirect(url_for('get_courses'))
            except Exception as e:
                db.session.rollback()
                print(e)
                abort(422)
            finally:
                db.session.close()
        else:
            abort(404)

    #  ----------------------------------------------------------------
    #  Tree  Endpoints
    #  ----------------------------------------------------------------

    '''
    ENDPOINT: Handles GET requests for trees,
    Returns: a list of trees, number of total trees,
    success true or not.

    TEST: Click the `Trees` Button to see the list of trees.

    curl "http://127.0.0.1:5000/trees

    '''

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
            '''
            return jsonify({
                'success': True,
                'count': len(trees),
                'data': data
            })
            '''
            return render_template('trees.html', trees=data)
        except Exception:
            abort(422)

    '''
    ENDPOINT: Handles GET request for 1 tree location.,
    Returns: tree details (name,type,location) + past and upcoming
        event information

    TEST: Click a tree name link.

    curl "http://127.0.0.1:5000/trees/1"

    '''
    
    @app.route('/trees/<int:id>', methods=['GET'])
    def show_tree(id):

        tree = Tree.query.filter(Tree.id == id).one_or_none()
        if tree:
            try:
                data = []
                u_events = db.session.query(Event).filter(
                    Event.tree_id == id).filter(
                    Event.course_date > datetime.now()).all()
                print("  my ", len(u_events), " upcoming events", u_events)
                print(len(u_events), "is the length of upcoming events")
                p_events = db.session.query(Event).filter(
                    Event.tree_id == id).filter(
                    Event.course_date < datetime.now()).all()
                print("  my ", len(p_events), " past events", p_events)
                print(len(p_events), "is the length of past events")

                upcoming_events = []
                for event in u_events:
                    # print(event, " is the event")
                    teacher = db.session.query(Teacher).filter(
                        Teacher.id == event.teacher_id).all()
                    course = db.session.query(Course).filter(
                        Course.id == event.course_id).all()
                    # print(type(course), " is the length of the course")
                    if len(teacher) > 0:
                        upcoming_events.append({
                            "teacher_id": teacher[0].id,
                            "teacher_name": teacher[0].name,
                            "teacher_img_url": teacher[0].img_url,
                            "course_id": course[0].id,
                            "course_date": event.course_date,
                            "course_name": course[0].name,
                            "course_level": course[0].course_level,

                        })

                past_events = []
                for event in p_events:
                    # print(event, " is the event")
                    teacher = db.session.query(Teacher).filter(
                        Teacher.id == event.teacher_id).all()
                    course = db.session.query(Course).filter(
                        Course.id == event.course_id).all()
                    if len(teacher) > 0:
                        past_events.append({
                            "teacher_id": teacher[0].id,
                            "teacher_name": teacher[0].name,
                            "teacher_img_url": teacher[0].img_url,
                            "course_id": course[0].id,
                            "course_date": event.course_date,
                            "course_name": course[0].name,
                            "course_level": course[0].course_level,

                        })
                # print("upcoming events, past events", upcoming_events, past_events)
                data.append({
                    "id": tree.id,
                    "name": tree.name,
                    "tree_type": tree.type,
                    "tree_location": tree.location,
                    "tree_img_url": tree.img_url,
                    "upcoming_events": upcoming_events,
                    "past_events": past_events,
                    "past_events_count": len(p_events),
                    "upcoming_events_count": len(u_events)
                })

                print(
                    "Upcoming Events \n",
                    len(upcoming_events),
                    upcoming_events)
                print("Past Events \n", len(past_events), past_events)
                '''
                return jsonify({
                    "success": True,
                    "data": data
                })
                '''
                return render_template('show_tree.html', tree=data[0])

                # print(data[0].temperament, " is the temperament")

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

    ''' Render add tree form '''

    
    @app.route('/trees/add', methods=['GET'])
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth('post:trees')
    def retrieve_new_tree_form(payload):
        form = TreeForm()
        print("I am here")
        return render_template('forms/add_tree.html', form=form)

    '''
    Endpoint : POST a new yoga tree location,
    Requires: Tree name text, type, location.
    TEST:

    curl http://127.0.0.1:5000/trees/add
    -X POST
    -H "Content-Type: application/json"
    -d '{"name":"Figgy","type": "Fig", "location": "Scary Dog's Garden", 
        "img_url": "https://https://res.cloudinary.com/potatobug/image/upload/
        c_scale,w_360/v1611477610/tree_sm_haa5xk.jpg"}'

    '''

    @app.route('/trees/add',
               methods=['POST'])  # plural collection endpoint
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth('post:trees')
    def create_tree(payload):
        form = TreeForm(request.form)
        error = False
        try:
            tree = (
                Tree(
                    name=form.name.data,
                    type=form.tree_type.data,
                    location=form.location.data,
                    img_url=form.img_url.data
                )
            )
            db.session.add(tree)  # tree.insert()
            db.session.commit()
            tree_id = tree.id
            '''
            return jsonify({
                "success": True,
                "created": tree_id
            })
            '''
        except Exception as e:
            error = True
            db.session.rollback()
            flash('An error occurred. tree could not be listed.')
            print(e)
            abort(422)
        finally:
            db.session.close()
        if error:
            flash('Tree ' +
                  request.form['name'] + ' could not be listed.')
            return render_template('trees.html')
        else:
            flash('Tree ' + request.form['name'] + ' was added!')
            return redirect(url_for('show_tree', id=tree_id))

    ''' Render edit tree form '''

    @app.route('/trees/<int:id>/edit',
               methods=['GET'])  # plural collection endpoint
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth('patch:trees')
    def retrieve_tree_info(payload, id):
        tree = Tree.query.filter(Tree.id == id).one_or_none()
        print(tree.id, tree.name, tree.type, tree.location, "Tree Dats!")
        form = TreeForm(obj=tree)  # Populate form with tree
        return render_template('forms/edit_tree.html', form=form, tree=tree)

    '''
    Endpoint : PATCH (edit) a tree,
    Requires: tree name text, type, location.
    TEST: Click the Edit a tree button to open the form to edit a tree.

    curl http://127.0.0.1:5000/trees/2/edit
    -X PATCH
    -H "Content-Type: application/json"
    -d '{"name":"shady","type":"oak","location":"yonder park",
    "img_url":"https://res.cloudinary.com/potatobug/image/upload/c_scale,
    w_360/v1611477610/tree_sm_haa5xk.jpg"}'

    '''

    @app.route('/trees/<int:id>/edit',
               methods=['POST', 'PATCH'])  # plural collection endpoint
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth('patch:trees')
    def edit_tree(payload, id):
        tree = Tree.query.filter(Tree.id == id).one_or_none()
        form = TreeForm(obj=tree)  # Populate form with tree

        if tree:
            try:
                tree.name = form.name.data
                tree.type = form.type.data
                tree.location = form.location.data
                tree.img_url = form.img_url.data

                db.session.commit()
                tree_id = tree.id
                flash('tree ' + tree.name + ' was just updated!')
                '''return jsonify({
                    "success": True,
                    "modidifed": tree_id,
                    "name": tree.name,
                    "type": tree.type,
                    "location": tree.location,
                    "img_url": tree.img_url
                })'''
                return redirect(url_for('show_tree', id=tree_id))

            except Exception as e:
                db.session.rollback()
                flash('An error occurred. tree could not be listed.')
                print(e)
                abort(422)
            finally:
                db.session.close()
        else:
            abort(404)

    '''
    ENDPOINT : DELETE tree using a tree ID.
    TEST: Click the Delete button on the individual tree page.
    This should persist in the database & on page refresh.
    curl -X DELETE "http://127.0.0.1:5000/trees/2"

    '''
    @app.route('/trees/<int:id>', methods=['DELETE', 'POST'])
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth('delete:trees')
    def delete_tree(payload, id):
        tree = Tree.query.filter(Tree.id == id).one_or_none()
        print(tree, " is the tree")
        tree_name = tree.name
        if tree:
            try:
                tree_id = tree.id
                db.session.delete(tree)
                db.session.commit()
                '''return jsonify({
                    "success": True,
                    "delete": tree_id
                })'''
                flash('Tree ' + tree_name + ' was successfully deleted!')
                # return render_template('events.html')
                return redirect(url_for('get_trees'))
            except Exception as e:
                db.session.rollback()
                print(e)
                abort(422)
            finally:
                db.session.close()
        else:
            abort(404)

    #  ----------------------------------------------------------------
    #  Event Endpoints
    #  ----------------------------------------------------------------

    '''
    ENDPOINT: Handles GET requests for events,
    Returns: a list of events, number of total events,
    success true or not.

    TEST: Click the `Events` Button to see the list of events.

    curl "http://127.0.0.1:5000/events

    '''

    @app.route('/events')
    def get_events():
        # events = db.session.query(Event).all()
        events = Event.query.order_by(Event.course_date).all()

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
                "event_id": event.id,
                "course_id": event.course_id,
                "teacher_id": event.teacher_id,
                "tree_id": event.tree_id,
                "course_date": event.course_date,
                "teacher_name": teacher_name,
                "tree_name": tree_name,
                "course_name": course_name,
                # "teacher_image_link": teacher_image_link
            })
        '''
        return jsonify({
            'success': True,
            'count': len(events),
            'data': data
            })
        '''
        return render_template('events.html', events=data)

    ''' Render add an event form '''

    @app.route('/events/create', methods=['GET'])
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth('post:events')
    def retrieve_new_event_form(payload):
        form = EventForm()
        print("I am here")
        return render_template('forms/add_event.html', form=form)

    '''
    Endpoint : POST an event,
    Requires: teacher id, course id, tree id (autopopulated dropdown in form), date
    TEST: Click Add an event button to open the form to add an event.
        Available values are selected via dropdown. Date selected by end-user.

    curl http://127.0.0.1:5000/events/add
    -X POST
    -H "Content-Type: application/json"
    -d '{"teacher_id":2,"course_id":2,"tree_id":2, "date":"2021-03-31 22:36:28"}'

    '''

    @app.route('/events/add',
               methods=['POST'])  # plural collection endpoint
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth('post:events')
    def create_event(payload):
        form = EventForm(request.form)
        teacher_name = form.teacher.data.name
        course_name = form.course.data.name
        tree_name = form.tree.data.name
        # form.teacher.query = Teacher.query.filter(Teacher.id > 0)
        # form.course.query = Course.query.filter(Course.id > 0)
        # form.tree.query = Tree.query.filter(Tree.id > 0)

        error = False
        try:

            teacher = Teacher.query.filter(
                Teacher.name == form.teacher.data.name).one_or_none()
            course = Course.query.filter(
                Course.name == form.course.data.name).one_or_none()
            tree = Tree.query.filter(
                Tree.name == form.tree.data.name).one_or_none()
            print(form.course_date.data, " is the course date")
            event = Event(
                teacher_id=teacher.id,
                course_id=course.id,
                tree_id=tree.id,
                course_date=form.course_date.data)
            db.session.add(event)  # teacher.insert()
            db.session.commit()
            event_id = event.id
            flash('Event was just added!')
            '''return jsonify({
                "success": True,
                "created": event_id
            })'''
        except Exception as e:
            error = True
            db.session.rollback()
            flash('An error occurred. Event could not be listed.')
            print(e)
            abort(422)
        finally:
            db.session.close()
        if error:
            flash('Event could not be listed.')
            return render_template('events.html')
        else:
            flash('Event ' + str(event_id) +
                  '-->  ' + course_name +
                  '  with teacher ' + teacher_name +
                  ' at ' + tree_name + ' tree was listed!')
            return redirect(url_for('get_events'))

    ''' Render edit an event form '''

    @app.route('/events/<int:id>/edit',
               methods=['GET'])  # plural collection endpoint
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth('patch:events')
    def retrieve_event_info(payload, id):
        event = Event.query.filter(Event.id == id).one_or_none()
        form = EventForm(obj=event)  # Populate form with course
        teacher = Teacher.query.filter(
            Teacher.id == event.teacher_id).one_or_none()
        course = Course.query.filter(
            Course.id == event.course_id).one_or_none()
        tree = Tree.query.filter(Tree.id == event.tree_id).one_or_none()
        return render_template(
            'forms/edit_event.html',
            form=form,
            event=event,
            teacher=teacher,
            course=course,
            tree=tree)

    '''
    Endpoint : PATCH (edit) a event,
    Requires: teacher id, course id, tree id (autopopulated dropdown in form), date
    TEST: Click Edit an event button to open the form to edit an event.
        Current event values are shown. Available values are selected via dropdown.

    curl http://127.0.0.1:5000/events/2/edit
    -X PATCH
    -H "Content-Type: application/json"
    -d '{"teacher_id":2,"course_id":2,"tree_id":2, "course_date":"2021-03-31 22:36:28"}'

    '''

    @app.route('/events/<int:id>/edit',
               methods=['POST', 'PATCH'])  # plural collection endpoint
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth('patch:events')
    def edit_event(payload, id):
        event = Event.query.filter(Event.id == id).one_or_none()
        form = EventForm(request.form)  # Populate form with course
        print(event.id, " is the event id")

        if form.teacher.data:
            teacher_name = form.teacher.data.name
        else:
            teacher = Teacher.query.filter(event.teacher_id == Teacher.id)[0]
            teacher_name = teacher.name
        if form.course.data:
            course_name = form.course.data.name
        else:
            course = Course.query.filter(event.course_id == Course.id)[0]
            course_name = course.name
        if form.tree.data:
            tree_name = form.tree.data.name
        else:
            tree = Tree.query.filter(event.tree_id == Tree.id)[0]
            tree_name = tree.name

        print(teacher_name)
        print(course_name)
        print(tree_name)
        print(event.id, "event id")

        # teacher_name = form.teacher.data.name
        # course_name = form.course.data.name
        # tree_name = form.tree.data.name

        if event:
            try:
                teacher = Teacher.query.filter(
                    Teacher.name == teacher_name).one_or_none()
                print(teacher.name, " is the teacher !!!!!", teacher.id)
                course = Course.query.filter(
                    Course.name == course_name).one_or_none()
                print(course.name, " is the coure !!!!!", course.id)
                tree = Tree.query.filter(Tree.name == tree_name).one_or_none()
                print(tree.name, " is the tree !!!!!", tree.id)
                print(teacher.id, course.id, tree.id, "latest stats")
                event.teacher_id = teacher.id
                event.course_id = course.id
                event.tree_id = tree.id
                event.course_date = form.course_date.data
                '''
                event = Event(
                    teacher_id=teacher.id,
                    course_id=course.id,
                    tree_id=tree.id,
                    course_date=form.course_date.data)
                '''
                print(event.id, " is the event.id")
                # db.session.add(event)  # teacher.insert()
                db.session.commit()
                # event_id = event.id
                print("and here's the latest event.id to check", event.id)
                '''return jsonify({
                    "success": True,
                    "modidifed": event.id,
                    "event_date": event.date
                })'''
                flash('Event was successfully updated!')
                # return render_template('events.html')
                return redirect(url_for('get_events'))

            except Exception as e:
                db.session.rollback()
                flash('An error occurred. Event could not be listed.')
                print(e)
                abort(422)
            finally:
                db.session.close()
                print("hallellllllooooyaaaa")
        else:
            abort(404)

    '''
    ENDPOINT : DELETE event using a event ID.
    TEST: Click the Delete button on the event listing or individual event page.
    This should persist in the database & on page refresh.
    curl -X DELETE "http://127.0.0.1:5000/events/2"

    '''

    @app.route('/events/<int:id>', methods=['DELETE', 'POST'])
    @cross_origin(headers=["Content-Type", "Authorization"])
    @requires_auth('delete:events')
    def delete_event(payload, id):
        event = Event.query.filter(Event.id == id).one_or_none()

        if event:
            try:
                event_id = event.id
                db.session.delete(event)
                db.session.commit()
                '''return jsonify({
                    "success": True,
                    "delete": event_id
                })'''
                flash('Event was successfully deleted!')
                # return render_template('events.html')
                return redirect(url_for('get_events'))
            except Exception as e:
                db.session.rollback()
                print(e)
                abort(422)
            finally:
                db.session.close()
        else:
            abort(404)

    # --------------------------------------------------------------------- #
    # @app.errorhandler decoratior to format error responses as JSON objects
    # for status codes: 401, 403 (Autherrors), 404 (not found),
    # 422 (unprocessable entity)
    # --------------------------------------------------------------------- #

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    '''
    404 : resource not found
    '''

    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    '''
    400 :
    '''

    @app.errorhandler(400)
    def unprocessable(error):
        return render_template('index.html', userinfo='')
        '''
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400
        '''

    '''
    AuthErrors - 401 : unauthorized
                403 : forbidden
    '''

    @app.errorhandler(401)
    def auth_error(error):
        print("I'm in auth error 401 I should be logged in")
        return render_template('index.html', userinfo=session['profile'])
        '''
        return jsonify({
            "success": False,
            "error": 401,
            "message": "unauthorized"
        }),  401
        '''

    @app.errorhandler(AuthError)
    def auth_error(ex):
        print(ex.error['code'], "is the code")
        print(ex.status_code, "is the status code")
        return jsonify({
            "success": False,
            "error": ex.status_code,
            "message": ex.error['code']
        }), ex.status_code  # 403 status code

    return app


app = create_app()
#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=env.get('PORT', 5000))
