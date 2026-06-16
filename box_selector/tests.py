from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Box
from .services import select_box

class BoxSelectionTests(TestCase):
    def setUp(self):
        # Create standard boxes
        self.box_small = Box.objects.create(
            name="Small Box", length=Decimal('10.0'), width=Decimal('10.0'), height=Decimal('10.0'), 
            max_weight_capacity=Decimal('2.0'), cost=Decimal('10.0')
        )
        self.box_medium = Box.objects.create(
            name="Medium Box", length=Decimal('20.0'), width=Decimal('20.0'), height=Decimal('20.0'), 
            max_weight_capacity=Decimal('5.0'), cost=Decimal('25.0')
        )
        self.box_heavy = Box.objects.create(
            name="Heavy Small Box", length=Decimal('12.0'), width=Decimal('12.0'), height=Decimal('12.0'), 
            max_weight_capacity=Decimal('20.0'), cost=Decimal('40.0')
        )
        self.box_long = Box.objects.create(
            name="Long Box", length=Decimal('50.0'), width=Decimal('10.0'), height=Decimal('10.0'), 
            max_weight_capacity=Decimal('5.0'), cost=Decimal('35.0')
        )
        
        self.client = APIClient()
        self.url = reverse('recommend_box_api')

    def test_happy_path(self):
        """Happy Path: Small order fits perfectly into a small, cheap box."""
        items = [{
            'name': 'Small Book', 'length': '8.0', 'width': '8.0', 'height': '2.0', 'weight': '0.5', 'quantity': 1
        }]
        box = select_box(items)
        self.assertEqual(box, self.box_small)
        
        # Test API
        response = self.client.post(self.url, {'items': items}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['box']['name'], "Small Box")

    def test_weight_limit(self):
        """Weight Limit Test: Small size but heavy, forcing a larger/stronger expensive box."""
        items = [{
            'name': 'Dumbbell', 'length': '8.0', 'width': '8.0', 'height': '8.0', 'weight': '15.0', 'quantity': 1
        }]
        box = select_box(items)
        # It's small enough for box_small, but 15kg > 2kg capacity.
        # So it should go to box_heavy (capacity 20kg).
        self.assertEqual(box, self.box_heavy)
        
    def test_dimensions_test(self):
        """Dimensions Test: Item is long but light, shouldn't fit in small square box."""
        items = [{
            'name': 'Poster Tube', 'length': '45.0', 'width': '5.0', 'height': '5.0', 'weight': '0.2', 'quantity': 1
        }]
        box = select_box(items)
        # Volume is 1125, small box is 1000. Medium box is 8000 but length is 20. 
        # Must use Long Box.
        self.assertEqual(box, self.box_long)
        
    def test_edge_case_too_large(self):
        """Edge Case: An order too heavy or large for any available box."""
        items = [{
            'name': 'Giant Statue', 'length': '100.0', 'width': '100.0', 'height': '100.0', 'weight': '50.0', 'quantity': 1
        }]
        box = select_box(items)
        self.assertIsNone(box)
        
        # Test API returns 404 error
        response = self.client.post(self.url, {'items': items}, format='json')
        self.assertEqual(response.status_code, 404)
        self.assertFalse(response.data['success'])

    def test_multiple_quantities_volume(self):
        """Test multiple items exceeding the volume of small box."""
        items = [{
            'name': 'Cubes', 'length': '8.0', 'width': '8.0', 'height': '8.0', 'weight': '0.5', 'quantity': 3
        }]
        box = select_box(items)
        # 1 cube is 512 volume. 3 cubes is 1536 volume. Small box max volume is 1000.
        # Total weight 1.5kg < 2kg capacity of small box.
        # Should upgrade to Medium box (cheaper than Heavy Small box, volume 8000).
        self.assertEqual(box, self.box_medium)
