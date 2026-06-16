from django.db import models

class Product(models.Model):
    """
    Represents an item available in the ecommerce store.
    """
    name = models.CharField(max_length=255)
    length = models.DecimalField(max_digits=10, decimal_places=2, help_text="in centimeters (cm)")
    width = models.DecimalField(max_digits=10, decimal_places=2, help_text="in centimeters (cm)")
    height = models.DecimalField(max_digits=10, decimal_places=2, help_text="in centimeters (cm)")
    weight = models.DecimalField(max_digits=10, decimal_places=2, help_text="in kilograms (kg)")

    def __str__(self):
        return self.name

    @property
    def volume(self):
        return self.length * self.width * self.height


class Box(models.Model):
    """
    Represents physical shipping boxes available in the warehouse.
    """
    name = models.CharField(max_length=100, unique=True)
    length = models.DecimalField(max_digits=10, decimal_places=2, help_text="Internal length in cm")
    width = models.DecimalField(max_digits=10, decimal_places=2, help_text="Internal width in cm")
    height = models.DecimalField(max_digits=10, decimal_places=2, help_text="Internal height in cm")
    max_weight_capacity = models.DecimalField(max_digits=10, decimal_places=2, help_text="Max weight in kg")
    cost = models.DecimalField(max_digits=10, decimal_places=2, help_text="Cost of the box in INR (₹)")

    class Meta:
        verbose_name_plural = "Boxes"
        ordering = ['cost']  # Always default sorting by cheapest first

    def __str__(self):
        return f"{self.name} (₹{self.cost})"

    @property
    def volume(self):
        return self.length * self.width * self.height


class Order(models.Model):
    """
    Represents a customer order.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    # The selected box will be calculated and populated via our service later
    assigned_box = models.ForeignKey(Box, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    """
    M2M Through relationship joining Orders and Products with a quantity.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in Order #{self.order.id}"
