import unittest
from app import app
from app.application import App
from app.models import User
from app.models import Bucket


class TestApplicationRoutes(unittest.TestCase):
    """
    This class contains tests for the application routes.
    """

    def setUp(self):
        """
        This method activates the flask testing config flag, which disables
        error catching during request handling.
        The testing client always provided an interface to the application.
        :return: 
        """
        app.testing = True
        self.app = app.test_client()
        self.application = App()
        #app.secret_key = "sdgsdgsjbdvskdxljvs"
        app.secret_key = 'ecii22727271sf@kdkdk'

    ## Test to see if the login page can be loaded.
    def test_login_status_code(self):
        response = self.app.get('/', content_type="html/text")
        self.assertEqual(response.status_code, 200, msg="Request was unsuccessful")
    
    ## Test if the signup page can be loaded.
    def test_signup_status_code(self):
        response = self.app.get('/signup', content_type="html/text")
        self.assertEqual(response.status_code, 200, msg="Request was unsuccessful")

    ## Test if dashboard loads successfully
    def test_dashboard_status_code(self):
        response = self.app.get('/dashboard', content_type="html/text")
        self.assertEqual(response.status_code, 200, msg="Request was unsuccessful")

    
    def test_bucket_status_code(self):
        response = self.app.get('/bucket', content_type="html/text")
        self.assertEqual(response.status_code, 200, msg="Request was unsuccessful")

    
    def test_bucketItem_status_code(self):
        response = self.app.get('/bucket_items', content_type="html/text")
        self.assertEqual(response.status_code, 200, msg="Request was unsuccessful")

    def test_sign_up_page_loads(self):
        response = self.app.get('/signup', content_type="html/text")
        self.assertTrue(b'Sign Up' in response.data)

    def test_login_page_loads(self):
        response = self.app.get('/login', content_type="html/text")
        self.assertTrue(b'Login' in response.data)


    ## Testing account existence.
    def test_user_existence(self):
        data=dict(username='chadwalt', password='chadwalt123')
        response = self.app.post('/login',data , follow_redirects=True)
        self.assertIn(b'No account found, please sign up first', response.data)

    # Testing for logging out.
    def test_user_logout(self):
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'login', response.data)

    # Testing for page not found if the user vists a wrong page.
    def test_404_page(self):
        response = self.app.get('/timo', follow_redirects=True)
        self.assertIn(b'Page Not Found', response.data)


if __name__ == '__main__':
    unittest.main()