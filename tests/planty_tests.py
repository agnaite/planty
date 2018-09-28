import os
import sys
import bcrypt 

topdir = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(topdir)

from planty import app
from planty.models import db, connect_to_db, User
from flask import session
import unittest

class PlantyTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        connect_to_db(app, 'postgresql:///planty-test')

        db.create_all()
        seed_test_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_login_and_logout(self):
        with self.client as c:
            # user does not exist
            result = c.post('/process_login',
                            data={'username': 'hacker', 'password': 'hack0r'},
                            follow_redirects=True)
            
            self.assertEqual(result.status_code, 200)
            self.assertEqual(b'error', result.data)
            self.assertTrue('logged_in' not in session)
        
            # user exists
            result = c.post('/process_login',
                            data={'username': 'agne', 'password': 'password'},
                            follow_redirects=True)
            
            
            self.assertEqual(result.status_code, 200)
            self.assertTrue('logged_in' in session)
            self.assertEqual(session['logged_in'], 1)
    
            result = c.get('/process_logout')
            
            self.assertEqual(b'logged out', result.data)
            self.assertTrue('logged_in' not in session)

def seed_test_data():
    user = User(username='agne', 
                password=bcrypt.hashpw('password'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
                email='agne@gmail.com',
                first_name='agne',
                last_name='klimaite',
                phone='4079139090')

    db.session.add(user)
    db.session.commit()
       
if __name__ == '__main__':
    unittest.main()

