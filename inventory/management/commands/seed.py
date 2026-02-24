from django.core.management.base import BaseCommand
from inventory.models import Warehouse, Product, StockItem
from decimal import Decimal
import random


class Command(BaseCommand):
    help = "Generira testne podatke za inventar"

    def handle(self, *args, **options):
        # Warehouses
        wh_data = [
            ("Glavno skladište", "Zagreb", 1000),
            ("Područno skladište 1", "Rijeka", 500),
            ("Područno skladište 2", "Split", 600),
        ]

        warehouses = []
        for name, city, capacity in wh_data:
            w, _ = Warehouse.objects.get_or_create(
                name=name,
                defaults={"city": city, "capacity": capacity},
            )
            # ako već postoji, ažuriraj city/capacity da seed bude determinističan
            w.city = city
            w.capacity = capacity
            w.save()
            warehouses.append(w)

        # Products
        products_data = [
            ("P001", "Monitor", Decimal("199.99"), 5),
            ("P002", "Miš", Decimal("19.99"), 10),
            ("P003", "Tipkovnica", Decimal("49.99"), 8),
            ("P004", "Grafička kartica", Decimal("499.99"), 2),
            ("P005", "Laptop", Decimal("899.99"), 3),
            ("P006", "USB stick", Decimal("9.99"), 15),
        ]

        products = []
        for sku, name, price, reorder_level in products_data:
            p, _ = Product.objects.get_or_create(
                sku=sku,
                defaults={"name": name, "price": price, "reorder_level": reorder_level},
            )
            p.name = name
            p.price = price
            p.reorder_level = reorder_level
            p.save()
            products.append(p)

        # Stock items (warehouse+product je unique, pa koristimo get_or_create)
        updated = 0
        for w in warehouses:
            for p in products:
                qty = random.randint(0, 30)
                s, created = StockItem.objects.get_or_create(
                    warehouse=w,
                    product=p,
                    defaults={"quantity": qty},
                )
                if not created:
                    s.quantity = qty
                    s.save()
                updated += 1

        self.stdout.write(self.style.SUCCESS(f"Seed gotov. Kreirano/ažurirano {updated} stavki zaliha."))