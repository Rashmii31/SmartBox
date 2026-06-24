from decimal import Decimal
from typing import List, Dict, Any
from abc import ABC, abstractmethod
from .models import Box

class ItemModifier(ABC):
    """Base interface for applying business rules to items before packing."""
    @abstractmethod
    def apply(self, item: Dict[str, Any]) -> Dict[str, Any]:
        pass

class FragilePaddingModifier(ItemModifier):
    """Adds 2cm padding on all sides (4cm total per dimension) for fragile items."""
    def apply(self, item: Dict[str, Any]) -> Dict[str, Any]:
        if item.get('is_fragile', False):
            # Create a copy to avoid mutating the original input data
            modified_item = item.copy()
            padding = Decimal('4.0')
            modified_item['length'] = Decimal(modified_item['length']) + padding
            modified_item['width'] = Decimal(modified_item['width']) + padding
            modified_item['height'] = Decimal(modified_item['height']) + padding
            return modified_item
        return item

def apply_modifiers(items_data: List[Dict[str, Any]], modifiers: List[ItemModifier]) -> List[Dict[str, Any]]:
    processed = []
    for item in items_data:
        current_item = item.copy()
        for mod in modifiers:
            current_item = mod.apply(current_item)
        processed.append(current_item)
    return processed

def select_box(items_data: List[Dict[str, Any]]) -> Box:
    """
    Selects the cheapest available box that can fit all items in the order.
    
    items_data is a list of dictionaries, where each dict has:
    - length: Decimal
    - width: Decimal
    - height: Decimal
    - weight: Decimal
    - quantity: int
    - is_fragile: bool (optional)
    """
    modifiers = [FragilePaddingModifier()]
    processed_items = apply_modifiers(items_data, modifiers)

    total_weight = Decimal('0.0')
    total_volume = Decimal('0.0')

    # Calculate totals
    for item in processed_items:
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
        box_dims = sorted([box.length, box.width, box.height], reverse=True)
        
        can_fit_all = True
        for item in processed_items:
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
            return box

    # No suitable box found
    return None
