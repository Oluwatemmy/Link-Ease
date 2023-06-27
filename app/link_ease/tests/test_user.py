import unittest
from link_ease.extensions import db
from link_ease.models import User
from link_ease import create_app
from link_ease.utils.views import generate_reset_token
from datetime import datetime, timedelta
import bcrypt


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_file='test_settings.py')

        self.appctx = self.app.app_context()

        self.appctx.push()

        self.client = self.app.test_client()

        db.create_all()

    def tearDown(self):

        # Drop the database table and also remove the session
        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None


    def test_index(self):
        """
        Test that the index page loads correctly
        """
        response = self.client.get('/')
        assert response.status_code == 200


    def test_register(self):
        with self.app.test_request_context():
            with self.client as client:
                # Send a POST request to the register route
                response = client.post('/register', data={
                    'username': 'test_user',
                    'email': 'test@user.com',
                    'password': 'test_password',
                    'confirm_password': 'test_password'
                }, follow_redirects=True)

                # Check that the user was redirected to the login page
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'Login', response.data)

                # Check that the user was added to the database
                self.assertEqual(User.query.count(), 1)


    def test_login(self):
        with self.app.test_request_context():
            with self.client as client:
                # Send a POST request to the login route
                response = client.post('/login', data={
                    'email': 'test@user.com',
                    'password': 'test_password'
                }, follow_redirects=True)

                # Check that the user was redirected to the home page
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'Home', response.data)


    def test_logout(self):
        with self.app.test_request_context():
            with self.client as client:
                # Send a POST request to the login route
                response = client.post('/login', data={
                    'email': 'test@user.com',
                    'password': 'test_password'
                }, follow_redirects=True)

                # Check that the user was redirected to the home page
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'Home', response.data)

                # Send a GET request to the logout route
                response = client.get('/logout', follow_redirects=True)

                # Check that the user was redirected to the login page
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'Login', response.data)


    def test_password_reset_request(self):
        with self.app.test_request_context():
            with self.client as client:
                response = client.post('/reset-password', data={
                    'email': 'test@user.com'
                }, follow_redirects=True)
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'Login', response.data)


    def test_password_reset(self):
        with self.app.test_request_context():
            with self.client as client:
                # Create a user with a password reset token
                user = User(username='test_user', email='test@user.com')
                user.set_password('test_password')
                user.password_reset_token = generate_reset_token(25)
                user.password_reset_token_expiration = datetime.utcnow() + timedelta(minutes=30)
                db.session.add(user)
                db.session.commit()

                token = user.password_reset_token

                # Send a POST request to the reset password route
                response = client.post(f'/reset-password/{token}', data={
                    'password': 'new_password',
                    'confirm_password': 'new_password'
                }, follow_redirects=True)
                # Check that the user was redirected to the login page
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'Login', response.data)

                # Check that the user's password was updated
                user = User.query.filter_by(email='test@user.com').first()
                self.assertTrue(bcrypt.checkpw('new_password'.encode('utf-8'), user.password.encode('utf-8')))

                # Verify that the password reset token has been cleared
                self.assertIsNone(user.password_reset_token)

                # Verify that a password reset token cannot be used again
                response = client.post(f'/reset-password/{token}', data={
                    'password': 'another_password',
                    'confirm_password': 'another_password'
                }, follow_redirects=True)
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'Login', response.data)
