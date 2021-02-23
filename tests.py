import unittest
from flask_testing import TestCase
import json
from flask_sqlalchemy import SQLAlchemy
from flask import url_for, request
from app import create_app
from models import setup_db, Teacher, Course, Event, Tree


class BaseTestCase(unittest.TestCase):
    """This class represents the squirrel test case"""
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(self)
        #self.app = Flask(__name__)
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['TESTING'] = True
        self.database_name = "postgres_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.client = self.app.test_client()

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
        # new question object
        self.new_teacher = Teacher(
            name='Test_Teacher11',
            age=1,
            temperament='raw',
            moves=['outthere','highbounce','fling'],
            img_url="https://res.cloudinary.com/potatobug/image/upload/c_scale,e_brightness:7,w_180/e_sharpen:100/v1611551627/squirrel_rounded_ey5qgk.jpg"
            )

    def tearDown(self):
        """Executed after reach test"""
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()
    
    
    
    """ Using assert_template_used in getting front page """
    
    
    def test_greeting(self):
            print(self.app.import_name, " is the app while trying to use GET")
            #print(self.app.__dict__, " is the object")
            with self.app.test_client() as c:
                res = c.get('/')
                print(res.__dict__, " is the response")
                print(res._status, " is the status")
                self.assertEqual(res.status_code, 200)
                #self.app.assert_template_used('index.html')
                #self.assert_context("greeting", "Hello!")

    """Get Front Page """
    '''
    #method 2 of getting front page also doesn't work
    def test_main_page2(self):
        with self.app.test_client() as c:
            res = c.get('/')
            self.assertEqual(res.status_code, 200)
    

    """Get Teachers """
    def test_teachers(self):
        response = self.client.get('/teachers')
        self.assertEqual(response.status_code, 200)
        #self.assertIn(b'Kyle', response.data)

    """Add A Teacher"""

    def test_add_teacher(self):
        with self.app.test_client() as c:
            t = self.new_teacher
            self.db.session.add(t)
            self.db.session.commit()
            teacher = Teacher.query.filter(Teacher.name == "Test_Teacher11").one_or_none()
            teacher_id = teacher.id
            res = c.get(f'/teacher/{teacher_id}')
            self.assertEqual(res.status_code, 200)


    """Delete Test Teacher"""

    def test_delete_teacher(self):
        # this delete test can now be run repeatedly because it deletes
        # a question that was added in test_add_new_question test
        with self.app.test_client() as c:
            added_teacher = (Teacher.query.filter
                             (Teacher.name == self.new_teacher.name)
                             .one_or_none())
            print(added_teacher.name, " is the teacher name")
            res = c.delete('/teachers/' + str(added_teacher.id))
            teacher = Teacher.query.filter(Teacher.id
                                           == added_teacher.id).one_or_none()
            self.assertEqual(res.status_code, 200)
            self.assertEqual(teacher, None)  # make sure it no longer exists

    """Load Front Page"""
    
    def test_home(self):
        tester = self.app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        #self.assertEqual(response.data, b'Hello World!')
    
    
    
    def test_main_page(self):
        with self.app.test_request_context('/'):
            assert request.path == '/'
            res = self.client.get('/', content_type='html/text', follow_redirects=True)
            #data = json.loads(res.data)
            #assert res.request.path == '/index.html'
            self.assertEqual(res.status_code, 200)
            #self.assertIn(b'Hello this is the index', res.data)
    '''
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
    # https://stackoverflow.com/questions/60430463/test-failing-in-flask-unit-test-with-404-error

