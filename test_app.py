from app import app
from models import db, User
from unittest import TestCase

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UsersTestCase(TestCase):
    """Testing user routes in app.py"""

    def setUp(self):
        """Clean up any existing users."""

        User.query.delete()
        user = User(first_name = "Eie",
                    last_name = "Burton",
                    image_url = 'https://www.rithmschool.com/assets/team/matt-ef82c973342786517e2be61bddac38e8a6a1d57f852c1a2e19cd3d2242b277aa.jpg')
        
        db.session.add(user)
        db.session.commit()
        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()


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

    
    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("user_details for testing only", html)


    def test_process_edit_user(self):
        with app.test_client() as client:
            info = {
                'first_name': 'Test',
                'last_name': 'test2',
                'image_url': 'https://images.unsplash.com/photo-1612392062798-4117917fcc50?ixid=MnwxMjA3fDF8MHxlZGl0b3JpYWwtZmVlZHw5fHx8ZW58MHx8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60'
                }
            resp = client.post(f"/users/{self.user_id}/edit", data=info)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('edit user for testing only', html)
            self.assertIn('Test test2', html)


# to do add delete test