from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth import authenticate
from .models import User
from substitutes.models import Product
from .views import favorites_page, subscribe_page, connexion_page
from django.contrib import messages

from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException


class UserPageTestCase(TestCase):

    def setUp(self):

        # Sets the request factory
        self.factory = RequestFactory()

        # Creates the user for the tests
        self.user = User.objects.create_user(
            email="test@gmail.com", password="test123", first_name="test"
        )

    def test_user_page_returns_200(self):

        user_id = self.user.id

        # Gets the response from client
        response = self.client.get(reverse("users:user_page", args=(user_id,)))

        # Checking if status code is equal to 200
        self.assertEqual(response.status_code, 200)


class FavoritesPageTestCase(TestCase):

    def setUp(self):

        # Sets the request factory
        self.factory = RequestFactory()

        # Creates the user for the tests
        self.user = User.objects.create_user(
            email="test@gmail.com", password="test123", first_name="test"
        )
        self.user_id = self.user.id

        # Creates a product in db
        cafe = Product.objects.create(name="cafe", nutriscore="c")

        # Adds product to favorites
        self.user.favorites.add(cafe)

    def test_user_favorites_returns_200(self):

        # Sets the request
        self.request = self.factory.get(
            "/users/favorites",
            args=(self.user_id,)
        )

        # Sets which user should do the request
        self.request.user = self.user

        # Sends the request and stores the response
        response = favorites_page(self.request, self.user_id)

        # Checks the response's status code
        self.assertEqual(response.status_code, 200)

    def test_favorites_gets_deleted(self):

        # Creates user
        user = User.objects.create_user(
            email="delete_favorite@gmail.com",
            password="delfav123",
            first_name="delfav"
        )
        user_id = user.id

        # Authenticates user
        authenticate(username=user.email, password=user.password)

        # Creates a product in db
        coca = Product.objects.create(name="coca", nutriscore="e")

        # Adds product to favorites
        user.favorites.add(coca)

        # Fetches the users favorites
        self.favorites = Product.objects.filter(
            favorites__id__icontains=user_id
        )

        # Counts how many favorites the user has before deletion
        initial_count = self.favorites.count()

        # Gets the last favorite in query set
        for fav in self.favorites:
            favorite = fav

        # Checking if favorite is fetched
        self.assertTrue(favorite)

        # Sending post request that deletes favorite fom db
        data = {"product_id": favorite.id}
        request = self.factory.post(
            "/users/favorites/",
            data,
        )
        request.user = user
        favorites_page(request, user.id)

        # Fetches the users favorites
        self.favorites = Product.objects.filter(
            favorites__id__icontains=user_id
        )

        # Checks the new count
        new_count = self.favorites.count()

        # Checks if the product is deleted
        self.assertEqual(new_count, initial_count - 1)


class SubscribePageTestCase(TestCase):

    def setUp(self):

        # Sets the request factory
        self.factory = RequestFactory()

    def test_subscribe_page_returns_200(self):

        # Builds the request
        self.request = self.factory.get("/users/subscribe")

        # Gets the subscribe page and stores the response
        response = subscribe_page(self.request)

        # The the response's status code
        self.assertEqual(response.status_code, 200)

    def test_user_creation(self):

        # Gets all users
        all_users = User.objects.all()

        # Counts the users
        initial_count = all_users.count()

        # Builds the request for subscription
        self.request = self.factory.post(
            "/users/subscribe",
            {
                "email": "test@gmail.com",
                "first_name": "test",
                "password": "pass123"
            },
        )

        # Stores the resquest's messages
        self.request._messages = messages.storage.default_storage(self.request)

        # Sends the request and stores the response
        response = subscribe_page(self.request)

        # Checks the count of users after the request
        new_count = all_users.count()

        # Checks if a user was added to the db
        self.assertEqual(new_count, initial_count + 1)

        # Checks if the response's status code is 200
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


class SeleniumUser():

    def __init__(self, id, email, first_name, password):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.password = password


class SeleniumTestCase(TestCase):

    def setUp(self):

        self.user = SeleniumUser(
            "15",
            "test@gmail.com",
            "test",
            "test123"
        )

        # Sets driver options
        self.options = Options()

        # Uncheck to run tests without browser window
        # options.headless = True

        # Sets the driver
        # For production environment
        # self.browser = webdriver.Firefox(executable_path='/usr/local/bin/geckodriver', options=self.options)

        # For local environment
        self.browser = webdriver.Firefox(executable_path='D:\webdrivers\geckodriver.exe', options=self.options)

    def test_selenium_logic(self):

        # Browses to the connexion page production environment
        # self.browser.get('http://159.65.51.134:80/users/connexion/')

        # Browses to the connexion page local environment
        self.browser.get('http://127.0.0.1:8000/users/connexion/')

        # Fetches the email and password inputs
        email_input = self.browser.find_element(by=By.ID, value='email_input')
        password_input = self.browser.find_element(by=By.ID, value='password_input')

        # Fetches the latest user added


        # Inserts the email and password inputs
        email_input.send_keys(self.user.email)
        time.sleep(1)
        password_input.send_keys(self.user.password + Keys.RETURN)

        time.sleep(2)
        # Verifies if Pur Beurre is in the title of the page
        assert 'Pur Beurre' in self.browser.title

        # Get the users page

        # For production environment
        # browser.get('http://159.65.51.134:80/users/{}/')

        # For local environment
        self.browser.get('http://127.0.0.1:8000/users/{}/'.format(self.user.id))

        # Verifies if the user's first_name is on the page
        assert self.user.first_name in self.browser.page_source

        search_input = self.browser.find_element(by=By.ID, value="searchForm")
        search_input.send_keys("Granola" + Keys.RETURN)
        time.sleep(1)

        save_button = self.browser.find_element(by=By.ID, value="save")
        save_button.click()
        time.sleep(1)

        favorites_page_button = self.browser.find_element(by=By.ID, value="favorites")
        self.assertTrue(favorites_page_button)
        favorites_page_button.click()
        time.sleep(1)

        fav_img = self.browser.find_element(by=By.ID, value="fav-img")
        self.assertTrue(fav_img)
        fav_img.click()
        time.sleep(1)

        favorites_page_button = self.browser.find_element(by=By.ID, value="favorites")
        favorites_page_button.click()
        time.sleep(1)

        delete_favorite_button = self.browser.find_element(by=By.ID, value="delete-fav")
        delete_favorite_button.click()
        time.sleep(1)

        try:
            fav_img = self.browser.find_element(by=By.ID, value="fav-img")
            self.assertFalse(fav_img)
        except NoSuchElementException:
            pass

        time.sleep(5)

        self.browser.quit()









