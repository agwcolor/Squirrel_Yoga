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
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['TESTING'] = True
        #self.app.config['APPLICATION_ROOT'] = '/templates'
        self.database_name = "postgres_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        self.client = self.app.test_client()

        # binds the app to the current context
        with self.app.app_context():
            print(self.app, "is the app")
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            print(self.db, " is the db")
            print(self.app.url_map, " is the app url_map")

        self.img_url ="https://res.cloudinary.com/potatobug/image/upload/c_scale,e_brightness:7,w_180/e_sharpen:100/v1611551627/squirrel_rounded_ey5qgk.jpg"


    def tearDown(self):
        """Executed after reach test"""
        pass

        """Load Front Page"""
    def test_main_page(self):
        res = self.client.get('/index.html', content_type='html/text', follow_redirects=True)
        #data = json.loads(res.data)
        #assert res.request.path == '/index.html'
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Hello this is the index', res.data)
    '''
    #method 2 of getting front page also doesn't work
    def test_main_page2(self):
        with self.app.test_client() as c:
            response = c.get('/index.html')
            self.assertEquals(response.status_code, 200)
    '''
    
    """Add A Teacher"""
    def test_add_teacher(self):
        t = Teacher(name='Test_teacher',age=1,
                    temperament='raw',
                    moves=['outthere','highbounce','fling'],
                    img_url=self.img_url
                    )
        self.db.session.add(t)
        self.db.session.commit()
        teacher = Teacher.query.filter(Teacher.name == "Test_teacher").one_or_none()
        teacher_id = teacher.id
        res = self.client().get(f'/teacher/{teacher_id}')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
    # https://stackoverflow.com/questions/60430463/test-failing-in-flask-unit-test-with-404-error

