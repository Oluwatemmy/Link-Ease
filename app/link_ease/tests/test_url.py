import unittest
from link_ease.extensions import db
from link_ease.models import User, Link
from link_ease import create_app
from flask_login import current_user, login_user


class ShortenLinkTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_file='test_settings.py')

        self.appctx = self.app.app_context()

        self.appctx.push()

        self.client = self.app.test_client()

        db.create_all()

    def tearDown(self):

        # Drop the database table and also remove the session
        db.drop_all()

        db.session.remove()

        self.appctx.pop()

        self.app = None

        self.client = None


    def test_add_link(self):
        with self.app.test_request_context():
            with self.client as client:
                # Create a logged-in user object or fetch it from the database
                logged_in_user = User(username='test_user', email='test@user.com')

                # Set the logged-in user as the current_user
                login_user(logged_in_user)
                
                # Set up the form data for the request
                form_data = {
                    'long-url': 'https://example.com',
                    'custom-url': 'custom'
                }

                # Send a POST request to the add_link route
                response = client.post('/add_link', data=form_data, follow_redirects=True)

                # add link to the database
                link = Link(original_url=form_data['long-url'], custom_url=form_data['custom-url'], user_id=current_user.id)
                db.session.add(link)
                db.session.commit()

                # Check that the user was redirected to the dashboard page
                self.assertEqual(response.status_code, 200)

                # Check that the link was added to the database
                self.assertEqual(Link.query.count(), 1)
                link = Link.query.first()
                self.assertEqual(link.original_url, 'https://example.com')
                self.assertEqual(link.custom_url, 'custom')
                self.assertEqual(link.user_id, current_user.id)


    def test_redirect_to_url_with_custom_url(self):
        # Create a link with a custom URL
        link = Link(original_url='https://example.com', custom_url='custom')
        db.session.add(link)
        db.session.commit()

        # Send a GET request to the custom URL
        response = self.client.get('/' + link.custom_url)

        # Check that the response is a redirect to the original URL
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'https://example.com')

        # Check that the link's visits count is incremented
        self.assertEqual(link.visits, 1)

    
    def test_redirect_to_url_without_custom_url(self):
        # Create a link without a custom URL
        link = Link(original_url='https://example.com', short_url='abcd')
        db.session.add(link)
        db.session.commit()

        # Send a GET request to the custom URL
        response = self.client.get('/' + link.short_url)

        # Check that the response is a redirect to the original URL
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'https://example.com')

        # Check that the link's visits count is incremented
        self.assertEqual(link.visits, 1)


    def test_redirect_to_url_with_invalid_url(self):
        # Send a GET request to a non-existent custom URL
        response = self.client.get('/qwerty')

        # Check that the response is a 404
        self.assertEqual(response.status_code, 404)

    
    def test_stats_route(self):
        with self.app.test_request_context():
            with self.client as client:
                # Create a logged-in user object or fetch it from the database
                logged_in_user = User(username='test_user', email='test@user.com')
                logged_in_user.set_password('test_password')

                # Set the logged-in user as the current_user
                login_user(logged_in_user)

                # Create some links for the user
                link1 = Link(original_url='https://example.com', user=logged_in_user)
                link2 = Link(original_url='https://google.com', user=logged_in_user)
                link3 = Link(original_url='https://github.com', user=logged_in_user)
                db.session.add_all([link1, link2, link3])
                db.session.commit()

                # Send a GET request to the stats route
                response = self.client.get('/stats')

                # Check that the response status code is 200
                self.assertEqual(response.status_code, 200)

                # Check that the rendered template contains the links' information
                self.assertIn(b'https://example.com', response.data)
                self.assertIn(b'https://google.com', response.data)
                self.assertIn(b'https://github.com', response.data)


    def test_view_link_routes(self):
        with self.app.test_request_context():
            with self.client as client:
                # Create a logged-in user object or fetch it from the database
                logged_in_user = User(username='test_user', email='test@user.com')
                logged_in_user.set_password('test_password')

                # Set the logged-in user as the current_user
                login_user(logged_in_user)

                # Create a link for the user
                link = Link(original_url='https://example.com', user=logged_in_user)
                db.session.add(link)
                db.session.commit()

                # Test the view_link route
                response = self.client.get(f'/link/{link.id}', follow_redirects=True)
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'https://example.com', response.data)

                # Test the view_custom_link route
                link.custom_url = 'custom'
                db.session.commit()
                response = self.client.get(f'/link/custom/{link.custom_url}', follow_redirects=True)
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'https://example.com', response.data)
                self.assertIn(b'custom', response.data)

                # Test the view_short_link route
                link.custom_url = None
                link.short_url = 'short'
                db.session.commit()
                response = self.client.get(f'/link/short/{link.short_url}', follow_redirects=True)
                self.assertEqual(response.status_code, 200)
                self.assertIn(b'https://example.com', response.data)
                self.assertIn(b'short', response.data)


    def test_download_qr_code(self):
        with self.app.test_request_context():
            with self.client as client:
                # Create a logged-in user object or fetch it from the database
                logged_in_user = User(username='test_user', email='test@user.com')
                logged_in_user.set_password('test_password')  # Set a password for the user

                # Set the logged-in user as the current_user
                login_user(logged_in_user)

                # Create a link for the user
                link = Link(original_url='https://example.com', user=logged_in_user)
                db.session.add(link)
                db.session.commit()

                # Test the download_qr_code route
                response = self.client.get(f'/download/{link.short_url}', follow_redirects=True)
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.mimetype, 'image/png')
                self.assertEqual(response.headers['Content-Disposition'], f"attachment; filename=qr_code_{link.short_url if link.short_url else link.custom_url}.png")