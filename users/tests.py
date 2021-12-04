from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import User
from substitutes.models import Product
from .views import favorites_page, subscribe_page, connexion_page, user_page, logout_view
from django.contrib import messages
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import chromedriver_binary

class UserPageTestCase(TestCase):

    def setUp(self):

        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email="test@gmail.com", password="test123", first_name="test"
        )

    def test_user_page_returns_200(self):

        user_id = self.user.id
        response = self.client.get(reverse("users:user_page", args=(user_id,)))
        self.assertEqual(response.status_code, 200)

    def test_users_page_gets_username(self):

        # browser = webdriver.Chrome(ChromeDriverManager().install())
        options = Options()
        browser = webdriver.Firefox('/home/travis/build/Heightsdesign/pur_beurre_project/geckodriver')
        # Sets the driver
        # browser = webdriver.Chrome(options)
        time.sleep(5)
        # Browses to the connexion page
        browser.get('http://159.65.51.134:80/users/connexion/')
        # Fetches the email and password inputs
        email_input = browser.find_element(by=By.ID, value='email_input')
        password_input = browser.find_element(by=By.ID, value='password_input')
        # Inserts the email and password inputs
        email_input.send_keys("test@gmail.com")
        password_input.send_keys("test123" + Keys.RETURN)
        time.sleep(5)
        # Verifies if the user is connected
        self.assertTrue(self.user.is_authenticated)
        # Verifies if Pur  Beure is in the title of the page
        assert 'Pur Beurre' in browser.title

        self.user = User.objects.latest('date_added')
        user_id = self.user.id
        # Get the users pager
        browser.get('http://159.65.51.134:80/users/{}/'.format(user_id))
        time.sleep(5)

        # Verifies if the users username is in the page
        assert "test" in browser.page_source
        browser.quit()


class FavoritesPageTestCase(TestCase):
    def setUp(self):

        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email="test@gmail.com", password="test123", first_name="test"
        )

        self.user_id = self.user.id
        self.request = self.factory.get(
            "/users/favorites",
            args=(self.user_id,)
        )
        self.request.user = self.user

        # Creates a product in db
        cafe = Product.objects.create(name="cafe", nutriscore="c")

        # Adds product to favorites
        self.user.favorites.add(cafe)

    def test_user_favorites_returns_200(self):

        response = favorites_page(self.request, self.user_id)
        self.assertEqual(response.status_code, 200)


class SubscribePageTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_subscribe_page_returns_200(self):

        self.request = self.factory.get("/users/subscribe")
        response = subscribe_page(self.request)
        self.assertEqual(response.status_code, 200)

    def test_user_creation(self):

        all_users = User.objects.all()
        initial_count = all_users.count()
        self.request = self.factory.post(
            "/users/subscribe",
            {
                "email": "test@gmail.com",
                "first_name": "test",
                "password": "pass123"
            },
        )
        self.request._messages = messages.storage.default_storage(self.request)
        response = subscribe_page(self.request)
        new_count = all_users.count()

        self.assertEqual(new_count, initial_count + 1)
        self.assertEqual(response.status_code, 200)


class ConnexionPageTestCase(TestCase):

    def setUp(self):

        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email="test@gmail.com", password="test123", first_name="test"
        )

    def test_connexion_page_returns_200(self):

        self.request = self.factory.get("/users/connexion/")
        response = connexion_page(self.request)
        self.assertEqual(response.status_code, 200)

    def test_login_successful(self):

        self.request = self.factory.post(
            "/users/connexion/",
            {"email": self.user.email, "password": self.user.password},
        )
        self.request._messages = messages.storage.default_storage(self.request)
        self.assertTrue(self.user.is_authenticated)

    def test_thank_you_page_returns_200(self):

        self.request = self.factory.post(
            "/users/connexion/",
            {"email": self.user.email, "password": self.user.password},
        )
        self.request._messages = messages.storage.default_storage(self.request)
        request = self.factory.get("/users/thank_you.html")
        response = connexion_page(self.request)
        self.assertEqual(response.status_code, 200)


class LogOutTestCase(TestCase):
    def setUp(self):

        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email="test@gmail.com", password="test123", first_name="test"
        )
        self.request = self.factory.post(
            "/users/connexion/",
            {"email": self.user.email, "password": self.user.password},
        )
        self.request._messages = messages.storage.default_storage(self.request)

    def logout_successful(self):

        self.request = self.factory.get("/users/logout/")
        self.assertFalse(self.user.is_authenticated)

    def test_logout_page_returns_200(self):

        self.request = self.factory.get("/users/logout/")
        response = connexion_page(self.request)
        self.assertEqual(response.status_code, 200)


class UserTestCase(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            email="test@gmail.com", password="test123", first_name="test"
        )

        cafe = Product.objects.create(name="cafe", nutriscore="c")
        self.user.favorites.add(cafe)

    def test_create_user(self):

        all_users = User.objects.all()
        original_count = all_users.count()

        self.newuser = User.objects.create_user(
            email="test2@gmail.com", password="test223", first_name="test2"
        )
        new_count = all_users.count()
        self.assertEqual(new_count, original_count + 1)

