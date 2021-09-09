from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.test import Client
from .models import Categories, Product


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

        cafe = Product.objects.create(name="cafe", nutriscore="c")
        category = Categories.objects.create(name="boisson")
        cafe.categories.add(category)
        self.product = Product.objects.get(name="cafe")
    
    def test_detail_page_returns_200(self):

        response = self.client.get(reverse('substitutes:search', args=(f'?query={self.product.name}',)))
        self.assertEqual(response.status_code, 200)