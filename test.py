__author__ = 'KarthikWitty'

from rest import app
import unittest
import json


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        '''Initializing the Test Client by Importing the app'''
        self.app=app.test_client()
        self.app.testing=True
        self.app.config=True

    def tearDown(self):
        pass

    def test_home_path(self):
        '''Testing the Home Path whether it is linking or not'''
        response=self.app.get('/')
        self.assertEqual(response.status_code,200)

    def test_get_path(self):
        '''Testing the get method whether it renders the result or not'''
        response= self.app.get('/object/2',content_type="application/json")
        self.assertEqual(response.status_code,200)

    def test_post(self):
        '''Testing the Post method whether it is Inserting into the database'''
        response=self.app.post('/object',data=json.dumps(
            {
                "ID":20,
                "VALUE":"Python"
            }
        ),content_type="application/json")
        print (response.data)
        self.assertEqual(response.status_code,201)

if __name__ == '__main__':
    unittest.main()


