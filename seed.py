import os
import django
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SmartBox.settings")
django.setup()

from box_selector.models import Box

def seed_boxes():
    boxes_data = [
        {"name": "Small Box", "length": "10.0", "width": "10.0", "height": "10.0", "max_weight_capacity": "2.0", "cost": "10.00"},
        {"name": "Medium Box", "length": "20.0", "width": "20.0", "height": "20.0", "max_weight_capacity": "5.0", "cost": "150.00"},
        {"name": "Heavy Small Box", "length": "12.0", "width": "12.0", "height": "12.0", "max_weight_capacity": "20.0", "cost": "40.00"},
        {"name": "Long Box", "length": "50.0", "width": "10.0", "height": "10.0", "max_weight_capacity": "5.0", "cost": "35.00"},
        {"name": "Standard Large", "length": "40.0", "width": "30.0", "height": "20.0", "max_weight_capacity": "15.0", "cost": "125.50"},
    ]

    for data in boxes_data:
        box, created = Box.objects.get_or_create(
            name=data["name"],
            defaults={
                "length": Decimal(data["length"]),
                "width": Decimal(data["width"]),
                "height": Decimal(data["height"]),
                "max_weight_capacity": Decimal(data["max_weight_capacity"]),
                "cost": Decimal(data["cost"]),
            }
        )
        if created:
            print(f"Created {box.name}")
        else:
            print(f"{box.name} already exists")

if __name__ == "__main__":
    seed_boxes()
