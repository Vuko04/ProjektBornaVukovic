from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Warehouse, Product, StockItem


class ModelTests(TestCase):
    def test_create_models(self):
        w = Warehouse.objects.create(name="S1", city="Zg", capacity=100)
        p = Product.objects.create(sku="X1", name="Test", price=10, reorder_level=1)
        s = StockItem.objects.create(warehouse=w, product=p, quantity=5)

        self.assertEqual(w.name, "S1")
        self.assertEqual(p.sku, "X1")
        self.assertEqual(s.quantity, 5)

    def test_unique_stockitem_per_warehouse_product(self):
        w = Warehouse.objects.create(name="S1", city="Zg", capacity=100)
        p = Product.objects.create(sku="X1", name="Test", price=10, reorder_level=1)
        StockItem.objects.create(warehouse=w, product=p, quantity=5)

        with self.assertRaises(Exception):
            StockItem.objects.create(warehouse=w, product=p, quantity=3)


class AuthTests(TestCase):
    def test_home_requires_login(self):
        resp = self.client.get(reverse("home"))
        self.assertEqual(resp.status_code, 302)  # redirect na login

    def test_product_add_requires_login(self):
        resp = self.client.get("/products/add/")
        self.assertEqual(resp.status_code, 302)

    def test_logged_user_can_open_product_add(self):
        User.objects.create_user(username="u1", password="pass12345")
        self.client.login(username="u1", password="pass12345")
        resp = self.client.get("/products/add/")
        self.assertEqual(resp.status_code, 200)