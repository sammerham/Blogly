from app import app
from unittest import TestCase

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sqla_intro_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class UsersTestCase(TestCase):
    """Testing user routes in app.py"""

    def test_show_add_user_form(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("create_user for testing only", html)

    def test_process_add_form(self):
        with app.test_client() as client:
            info = {
                'first_name': 'Elie',
                'last_name': 'Burton',
                'image_url': 'https://www.rithmschool.com/assets/team/matt-ef82c973342786517e2be61bddac38e8a6a1d57f852c1a2e19cd3d2242b277aa.jpg'
                }
            resp = client.post("/users/new", data=info, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('user_list for testing only', html)
            self.assertIn('Elie Burton', html)
