from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import User
from substitutes.models import Product
from .views import favorites_page, subscribe_page, connexion_page
from django.contrib import messages


class UserPageTestCase(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(
            email="test@gmail.com", password="test123", first_name="test"
        )

    def test_user_page_returns_200(self):
        user_id = self.user.id
        response = self.client.get(reverse("users:user_page", args=(user_id,)))
        self.assertEqual(response.status_code, 200)


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


class LogOutTestCase(TestCase):
    def setUp(self):

        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email="test@gmail.com", password="test123", first_name="test"
        )


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
