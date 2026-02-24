from django.db import models


class Warehouse(models.Model):
    name = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} ({self.city})"


class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    reorder_level = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.sku} - {self.name}"


class StockItem(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="stock_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="stock_items")
    quantity = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["warehouse", "product"], name="unique_product_per_warehouse")
        ]

    def __str__(self):
        return f"{self.product.name} @ {self.warehouse.name} = {self.quantity}"