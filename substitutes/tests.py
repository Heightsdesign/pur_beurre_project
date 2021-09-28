from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import Categories, Product, Stores
from users.models import User
from .views import search
from django.contrib import messages


class IndexPageTestCase(TestCase):

    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class DetailPageTestCase(TestCase):

    def setUp(self):
        cafe = Product.objects.create(name="cafe", nutriscore="c")
        self.product = Product.objects.get(name="cafe")

    def test_detail_page_returns_200(self):
        product_id = self.product.id
        response = self.client.get(reverse('substitutes:detail', args=(product_id,)))
        self.assertEqual(response.status_code, 200)

    def test_detail_page_returns_404(self):
        product_id = self.product.id + 1
        response = self.client.get(reverse('substitutes:detail', args=(product_id,)))
        self.assertEqual(response.status_code, 404)


class SearchPageTestCase(TestCase):

    def setUp(self):

        self.factory = RequestFactory()

        # Creates user in db
        self.user = User.objects.create_user(
            email="test@gmail.com",
            password="test123",
            first_name="test"
        )

        # Gets user id
        self.user_id = self.user.id

        # Creates product 'cafe' in db
        cafe = Product.objects.create(name="cafe", nutriscore="c")

        # Creates category 'boisson' in db
        category = Categories.objects.create(name="boisson")

        # Adds category 'boisson' to cafe
        cafe.categories.add(category)

        # Gets Product object 'cafe' from db
        self.product = Product.objects.get(name="cafe")

        # Builds the request
        self.request = self.factory.get(f'/substitutes/search/?query={self.product.name}')
        self.request.user = self.user
    
    def test_detail_page_returns_200(self):

        # Gets the response
        response = search(self.request)
        self.assertEqual(response.status_code, 200)

    def test_product_is_added_to_favorites(self):

        # Checks the favorites of the user
        favorites = Product.objects.filter(favorites__id__icontains=self.user_id)

        # initialises count before insert (0)
        old_count = favorites.count()

        # Gets product id
        product_id = self.product.id

        # Builds the request
        self.request = self.factory.post(f'/substitutes/search/?query={self.product.name}', {'product_id': product_id})

        # Inserts the user in request
        self.request.user = self.user

        # Gets the messages
        self.request._messages = messages.storage.default_storage(self.request)

        # Gets the response
        response = search(self.request)

        # Checks the count after insertion (1)
        new_count = favorites.count()

        self.assertEqual(new_count, old_count + 1)

    def test_return_post_page_returns_200(self):

        favorites = Product.objects.filter(favorites__id__icontains=self.user_id)
        product_id = self.product.id
        self.request = self.factory.post(f'/substitutes/search/?query={self.product.name}', {'product_id': product_id})
        self.request.user = self.user
        self.request._messages = messages.storage.default_storage(self.request)
        response = search(self.request)
        self.assertEqual(response.status_code, 200)

    def test_error_template_returns_200(self):

        notExistingProduct = "caramel"
        self.request = self.factory.get(f'/substitutes/search/?query={notExistingProduct}')
        response = search(self.request)
        self.assertEqual(response.status_code, 200)


class ProductTestCase(TestCase):

    def setUp(self):

        cafe = Product.objects.create(
            name="cafe",
            nutriscore="c",
            key_100g="caffeine:70g",
            url="https//:www.openfoodfacts.com/cafe",
            imgurl="https//:www.openfoodfacts.com/img/cafe"
        )

        category = Categories.objects.create(name="boisson")
        cafe.categories.add(category)
        store = Stores.objects.create(name="Leclerc")
        cafe.stores.add(store)

    def test_get_product_name(self):

        product = Product.objects.get(name="cafe")
        self.assertEqual(product.name, "cafe")

    def test_get_product_nutriscore(self):

        product = Product.objects.get(name="cafe")
        self.assertEqual(product.nutriscore, "c")

    def test_get_product_category(self):

        product = Product.objects.get(name="cafe")
        categories = product.categories.all()
        self.assertEqual(categories.first().name, "boisson")

    def test_get_product_store(self):

        product = Product.objects.get(name="cafe")
        stores = product.stores.all()
        self.assertEqual(stores.first().name, "Leclerc")
