from django.core.management.base import BaseCommand, CommandError
import algorithm.db_and_objects.product as product
from substitutes.models import Product as DbProduct


class Command(BaseCommand):
    help = 'Insert data in a PostgreSQL database'

    def handle(self, *args, **options):

        prods = product.ProductParser().parser()
        manager = product.ProductManager(prods)
        manager.save_products()
        product.ProductManager('prods').delete_doubles(DbProduct)
