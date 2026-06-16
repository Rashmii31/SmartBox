from decimal import Decimal
from typing import List, Dict, Any
from .models import Box

def select_box(items_data: List[Dict[str, Any]]) -> Box:
    """
    Selects the cheapest available box that can fit all items in the order.
    
    items_data is a list of dictionaries, where each dict has:
    - length: Decimal
    - width: Decimal
    - height: Decimal
    - weight: Decimal
    - quantity: int
    """
    total_weight = Decimal('0.0')
    total_volume = Decimal('0.0')

    # Calculate totals
    for item in items_data:
        quantity = Decimal(item.get('quantity', 1))
        weight = Decimal(item['weight'])
        length = Decimal(item['length'])
        width = Decimal(item['width'])
        height = Decimal(item['height'])
        
        total_weight += weight * quantity
        total_volume += (length * width * height) * quantity

    # Get all available boxes (they are ordered by cost in the Meta class)
    boxes = Box.objects.all()

    for box in boxes:
        # 1. Check weight capacity
        if box.max_weight_capacity < total_weight:
            continue
        
        # 2. Check total volume
        if box.volume < total_volume:
            continue
            
        # 3. Check individual dimensions (3D fitting check)
        # An item must physically fit inside the box. 
        # We sort dimensions to handle arbitrary rotations.
        box_dims = sorted([box.length, box.width, box.height], reverse=True)
        
        can_fit_all = True
        for item in items_data:
            item_dims = sorted([
                Decimal(item['length']), 
                Decimal(item['width']), 
                Decimal(item['height'])
            ], reverse=True)
            
            # Check if this item fits in the box in any orientation
            if (item_dims[0] > box_dims[0] or 
                item_dims[1] > box_dims[1] or 
                item_dims[2] > box_dims[2]):
                can_fit_all = False
                break
                
        if can_fit_all:
            return box  # Since boxes are ordered by cost, the first fit is the cheapest

    # No suitable box found
    return None
