import unittest
from flask_testing import TestCase
import json
from flask_sqlalchemy import SQLAlchemy
from flask import url_for, request
from models import setup_db, Teacher, Course, Event, Tree
from app import create_app
unittest.TestLoader.sortTestMethodsUsing = None


class BaseTestCase(unittest.TestCase):
    """This class represents the squirrel test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(test_config=True)

        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['TESTING'] = True
        self.database_name = "postgres_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.client = self.app.test_client()

        # new teacher object

        self.new_teacher = {
            "name": "Test_Teacher",
            "age": 2, 
            "temperament": "sly", 
            "moves": ["outhere","highbounce","horizontal fling"], 
            "img_url": "https://res.cloudinary.com/potatobug/image/upload/c_scale,e_brightness:7,w_180/e_sharpen:100/v1611551627/squirrel_rounded_ey5qgk.jpg"
            }
        
        # new course object
        self.new_course = {
            "name": "Test_Course",
            "course_level": 5
        }

        # binds the app to the current context
        ctx = self.app.app_context()
        ctx.push()

        self.db = SQLAlchemy()
        self.db.init_app(self.app)
        # create all tables
        self.db.create_all()

        '''
        with self.app.app_context():
            print(self.app, "is the app")
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            print(self.db, " is the db")
            print(self.app.url_map, " is the app url_map")
        '''

    def tearDown(self):
        """Executed after each test"""
        pass
       
       
        
    '''
    """Get Front Page """

    def test_main_page(self):
            print(self.app.import_name, " is the app while trying to use GET")
            #print(self.app.__dict__, " is the object")
            with self.app.test_client() as c:
                res = c.get('/')
                #print(res.__dict__, " is the response")
                self.assertEqual(res.status_code, 200)


    """Get Teachers """
    def test_get_all_teachers(self):
        res = self.client.get('/teachers')
        print("\n",res.__dict__, " is the response")
        self.assertEqual(res.status_code, 200)
        #self.assertIn(b'Kyle', response.data)
    
    
    def test_404_request_beyond_valid_page(self):
        with self.app.test_client() as c:
            res = c.get('/teachers/1000')
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'resource not found')
    
    
    """Add (POST) Teachers """
    def test_add_new_teacher(self):
        with self.app.test_client() as c:
            res = c.post('/teachers/add',
                         data=dict(self.new_teacher),
                         follow_redirects=True)
            teacher = (Teacher.query.filter(Teacher.name == "Test_Teacher15")
                   .one_or_none())
            print("Teacher smeecher is", teacher.name)
            self.assertEqual(res.status_code, 200)  # status code
    
    
    def test_422_invalid_add_teacher(self):
        with self.app.test_client() as c:
            res =c.post('/teachers/add',
                         data=dict({"title":"",
                                    "age":"" ,
                                    "temperament":"",
                                    "moves": [], 
                                    "img_url": "five"
                                    }),
                         follow_redirects=True)
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 400)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'bad request')

    
    """Edit (PATCH) Teachers """
    def test_modify_teacher(self):
        with self.app.test_client() as c:
            res = c.post('/teachers/add',
                         data=dict(self.new_teacher),
                         follow_redirects=True)
            teacher = (Teacher.query.filter(
                Teacher.name == self.new_teacher["name"]).one_or_none())
            print("Teacher is", teacher.name, teacher.id)
            self.assertEqual(res.status_code, 200)  # status code
        with self.app.test_client() as c:
            print(self.new_teacher["name"])
            teacher = (Teacher.query.filter(Teacher.name == self.new_teacher["name"])
                   .one_or_none())
            print(teacher.name, "is where we are now ")
            res = c.patch('/teachers/'+str(teacher.id)+'/edit',
                         data=dict({"name": "Test_Teacher16",
                                    "age": 2,
                                    "temperament": "test_temperament",
                                    "moves": ["outhere","highbounce","horizontal fling"], 
                                    "img_url": "https://res.cloudinary.com/potatobug/image/upload/c_scale,e_brightness:7,w_180/e_sharpen:100/v1611551627/squirrel_rounded_ey5qgk.jpg"
                                    }),
                         follow_redirects=True)
            teacher = (Teacher.query.filter(Teacher.temperament == "test_temperament")
                   .one_or_none())
            print(teacher.temperament, " is test_temperament", teacher.name, teacher.id)
            self.assertEqual(res.status_code, 200)  # status code

    
    
    """Delete Test Teacher"""

    def test_delete_teacher(self):
        # this delete test can now be run repeatedly because it deletes
        # a teacher that was added in teacher test
        added_teacher = (Teacher.query.filter(
            Teacher.name == self.new_teacher["name"]).one_or_none())
        print(added_teacher.name)
        with self.app.test_client() as c:
            res = c.delete('/teachers/' + str(added_teacher.id),
                                              follow_redirects=True)
            teacher = Teacher.query.filter(Teacher.id
                                           == added_teacher.id).one_or_none()
            self.assertEqual(res.status_code, 200)
            self.assertEqual(teacher, None)  # make sure it no longer exists
    
    
    """Delete fails"""
    
    def test_404_delete_fail(self):
        with self.app.test_client() as c:
            res = c.delete('/teachers/1000')
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'resource not found')
    
    
    """Get Courses """
    def test_courses(self):
        res = self.client.get('/courses')
        #print("\n",res.__dict__, " is the response")
        self.assertEqual(res.status_code, 200)
        #self.assertIn(b'Kyle', response.data)
       
    """Add (POST) Courses """
    def test_add_new_course(self):
        with self.app.test_client() as c:
            res = c.post('/courses/add',
                         data=dict(self.new_course),
                         follow_redirects=True)
            teacher = (Course.query.filter(Course.name == "Test_Course")
                   .one_or_none())
            print("Course name is", course.name)
            self.assertEqual(res.status_code, 200)  # status code


    '''
    """Edit (PATCH) Courses """
    def test_modify_course(self):
        with self.app.test_client() as c:
            res = c.post('/courses/add',
                         data=dict(self.new_course),
                         follow_redirects=True)
            course = (Course.query.filter(
                Course.name == self.new_course["name"]).one_or_none())
            print("Course is", course.name, course.id)
            self.assertEqual(res.status_code, 200)  # status code
        with self.app.test_client() as c:
            print(self.new_course["name"])
            course = (Course.query.filter(Course.name == 
                                          self.new_course["name"]).one_or_none())
            print(course.name, "is where we are now ")
            res = c.patch('/courses/'+str(course.id)+'/edit',
                         data=dict({"name": "Test_Course",
                                    "course_level": 100,
                                    }),
                         follow_redirects=True)
            course = (Course.query.filter(Course.course_level == 100)
                   .one_or_none())
            print(course.course_level, " is 10", course.name, course.id)
            self.assertEqual(res.status_code, 200)  # status code
            
    
    """Delete Test Course"""

    def test_to_delete_course_that_was_added_in_order(self):
        # this delete test can now be run repeatedly because it deletes
        # a teacher that was added in teacher test
        added_course = (Course.query.filter(
            Course.name == self.new_course["name"]).one_or_none())
        print(added_course)
        with self.app.test_client() as c:
            res = c.delete('/courses/' + str(added_course.id),
                                              follow_redirects=True)
            course = Course.query.filter(Course.id
                                           == added_course.id).one_or_none()
            self.assertEqual(res.status_code, 200)
            self.assertEqual(course, None)  # make sure it no longer exists
        
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
