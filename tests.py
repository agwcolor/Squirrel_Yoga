import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import url_for, request


from app import create_app
from models import setup_db, Teacher, Course, Event, Tree


class BaseTestCase(unittest.TestCase):
    """This class represents the squirrel test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.app.config['WTF_CSRF_ENABLED'] = False
        #self.app.config['SERVER_NAME'] = "127.0.0.1:5432"  # fine
        self.app.config['TESTING'] = True
        self.database_name = "postgres_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # new teacher object
        '''
        self.new_teacher = Teacher(
            name='Rozo',
            age=1,
            temperament='raw',
            moves=['outthere','highbounce','fling'],
            img_url="https://res.cloudinary.com/potatobug/image/upload/c_scale,e_brightness:7,w_180/e_sharpen:100/v1611551627/squirrel_rounded_ey5qgk.jpg"
        )
        '''
        self.new_teacher = {
            'name': 'Rozo',
            'age': 1,
            'temperament': 'raw',
            'moves': ['outthere','highbounce','fling'],
            'img_url':"https://res.cloudinary.com/potatobug/image/upload/c_scale,e_brightness:7,w_180/e_sharpen:100/v1611551627/squirrel_rounded_ey5qgk.jpg"
        }
        
        # new course ojbect
        self.new_course = {
            'name': 'spin&bounce',
            'level': 3
        }

        # binds the app to the current context
        with self.app.app_context():
            #print(self.app, "is the app")
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Test for successful operation and for expected errors.
    """

    def test_get_all_teachers(self):
        res = self.client().get('/teachers')  # is client geting endpoint
        #data = json.loads(res.data)  # load data w/ json.loads as string
        self.assertEqual(res.status_code, 200)

    def test_add_new_teacher(self):
        res = self.client().post('/teachers/add', data=self.new_teacher)
        #print(res.data)
        #print(data, " is the data  ..........")
        print(res.get_json(), "hi")
        print(res.data, "h2")

        #data = res.get_json()
        #print(type(data))
        #question = (Question.query.filter(Question.id == data['created']).one_or_none())
        #teacher = (Teacher.query.filter(Teacher.name == self.new_teacher.name).one_or_none())

        self.assertEqual(res.status_code, 200)  # status code# is teacher created
        #print("created teacher", teacher.id)

    def test_main_page(self):
        res = self.client().get('/index.html', follow_redirects=True)
        #data = json.loads(res.data)
        #assert res.request.path == '/index.html'
        self.assertEqual(res.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
