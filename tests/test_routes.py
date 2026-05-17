import os
import logging
import unittest
from service import app
from service.common import status
from service.models import db, Product
from tests.factories import ProductFactory

DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///../development.db")
BASE_URL = "/products"

class TestProductRoutes(unittest.TestCase):
    """Product Service Route Test Cases"""

    @classmethod
    def setUpClass(cls):
        """Run once before all tests"""
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
        app.logger.setLevel(logging.CRITICAL)
        Product.init_db(app)

    @classmethod
    def tearDownClass(cls):
        """Run once after all tests"""
        db.session.close()

    def setUp(self):
        """Runs before each test"""
        db.drop_all()
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        """Runs after each test"""
        db.session.remove()
        db.drop_all()

    def _create_products(self, count):
        """Helper method to create products in bulk"""
        products = []
        for _ in range(count):
            test_product = ProductFactory()
            response = self.client.post(BASE_URL, json=test_product.serialize())
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            products.append(Product().deserialize(response.get_json()))
        return products

    # ----------------------------------------------------------------------
    # TEST CASES
    # ----------------------------------------------------------------------

    def test_get_product(self):
        """It should Get a single Product"""
        test_product = self._create_products(1)[0]
        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(data["name"], test_product.name)

    def test_update_product(self):
        """It should Update an existing Product"""
        test_product = ProductFactory()
        response = self.client.post(BASE_URL, json=test_product.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_product = response.get_json()
        new_product["description"] = "New Description Text"
        response = self.client.put(f"{BASE_URL}/{new_product['id']}", json=new_product)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_product = response.get_json()
        self.assertEqual(updated_product["description"], "New Description Text")

    def test_delete_product(self):
        """It should Delete a Product"""
        test_product = self._create_products(1)[0]
        response = self.client.delete(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(f"{BASE_URL}/{test_product.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_product_list(self):
        """It should Get a list of Products"""
        self._create_products(5)
        response = self.client.get(BASE_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), 5)

    def test_query_by_name(self):
        """It should Query Products by name"""
        products = self._create_products(5)
        test_name = products[0].name
        name_count = len([p for p in products if p.name == test_name])
        response = self.client.get(BASE_URL, query_string=f"name={test_name}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), name_count)

    def test_query_by_category(self):
        """It should Query Products by category"""
        products = self._create_products(10)
        category = products[0].category
        category_string = category.name
        category_count = len([p for p in products if p.category == category])
        response = self.client.get(BASE_URL, query_string=f"category={category_string}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), category_count)

    def test_query_by_availability(self):
        """It should Query Products by availability"""
        products = self._create_products(10)
        test_available = products[0].available
        available_count = len([p for p in products if p.available == test_available])
        response = self.client.get(BASE_URL, query_string=f"available={str(test_available)}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.get_json()
        self.assertEqual(len(data), available_count)