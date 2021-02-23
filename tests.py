import unittest
from flask_testing import TestCase
import json
from flask_sqlalchemy import SQLAlchemy
from flask import url_for, request
from models import setup_db, Teacher, Course, Event, Tree
from app import create_app


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
            "name":"Test_Teacher15",
            "age":2, 
            "temperament":"sly", 
            "moves":["outhere","highbounce","horizontal fling"], 
            "img_url":"https://res.cloudinary.com/potatobug/image/upload/c_scale,e_brightness:7,w_180/e_sharpen:100/v1611551627/squirrel_rounded_ey5qgk.jpg"
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
        """Executed after reach test"""
        pass


    """Get Front Page """

    def test_main_page(self):
            print(self.app.import_name, " is the app while trying to use GET")
            #print(self.app.__dict__, " is the object")
            with self.app.test_client() as c:
                res = c.get('/')
                #print(res.__dict__, " is the response")
                self.assertEqual(res.status_code, 200)


    """Get Teachers """
    def test_teachers(self):
        res = self.client.get('/teachers')
        print("\n",res.__dict__, " is the response")
        self.assertEqual(res.status_code, 200)
        #self.assertIn(b'Kyle', response.data)

    def test_add_new_teacher(self):
        with self.app.test_client() as c:
            res = c.post('/teachers/add',
                         data=dict(self.new_teacher),
                         follow_redirects=True)
            teacher = (Teacher.query.filter(Teacher.name == "Test_Teacher15")
                   .one_or_none())
            print("Teacher smeecher is", teacher.name)
            self.assertEqual(res.status_code, 200)  # status code


    """Delete Test Teacher"""

    def test_delete_teacher(self):
        # this delete test can now be run repeatedly because it deletes
        # a teacher that was added in teacher test
        with self.app.test_client() as c:
            added_teacher = (Teacher.query.filter
                             (Teacher.name == self.new_teacher["name"])
                             .one_or_none())
            print(added_teacher.name, " is the teacher to delete")
            res = c.delete('/teachers/' + str(added_teacher.id),
                                              follow_redirects=True)
            teacher = Teacher.query.filter(Teacher.id
                                           == added_teacher.id).one_or_none()
            self.assertEqual(res.status_code, 200)
            self.assertEqual(teacher, None)  # make sure it no longer exists


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
