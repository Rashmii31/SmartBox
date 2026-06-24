# Fragile Product Requirement Response

## Overview

Thank you for the follow-up evaluation task. The objective is to support "fragile products" in our AI-Assisted Box Selection System by requiring an additional 2 cm padding on every side before verifying if the item fits into a given warehouse box. 

To address this cleanly and efficiently, I analyzed the core packing algorithm in our application. My solution ensures backward compatibility, adheres strictly to the Open/Closed Principle (OCP), and decouples business-specific padding logic from the core 3D spatial fitting mechanism. Below is a detailed technical breakdown of my approach.

## Files and Components to Modify

To cleanly implement this requirement without muddying the existing logic, modifications target the following specific areas of the application:

1. **`box_selector/models.py`**
   - **Component:** `Product` model
   - **Reason:** To persist whether a specific product requires fragile packaging at the database level.
2. **`box_selector/services.py`**
   - **Component:** `select_box()` function and introduction of the `ItemModifier` interface.
   - **Reason:** To intercept items marked as fragile and mathematically inflate their dimensions (length, width, height) prior to executing the volume and physical fitting algorithm.
3. **`box_selector/views.py`**
   - **Component:** `BoxRecommendationAPI`
   - **Reason:** To update the example documentation payload showing API consumers how to pass the fragile flag.
4. **`box_selector/tests.py`**
   - **Component:** `BoxSelectionTests`
   - **Reason:** To validate the boundary conditions and ensure a fragile item shifts to a larger box.

## Proposed Changes

### 1. Database Model Updates
I am adding an `is_fragile` boolean flag to the `Product` model. By defaulting this to `False`, I ensure that all existing database entries and previous API requests remain fully backward compatible.

**Before:**
```python
class Product(models.Model):
    # ...
    height = models.DecimalField(max_digits=10, decimal_places=2, help_text="in centimeters (cm)")
    weight = models.DecimalField(max_digits=10, decimal_places=2, help_text="in kilograms (kg)")
```

**After:**
```python
class Product(models.Model):
    # ...
    height = models.DecimalField(max_digits=10, decimal_places=2, help_text="in centimeters (cm)")
    weight = models.DecimalField(max_digits=10, decimal_places=2, help_text="in kilograms (kg)")
    is_fragile = models.BooleanField(default=False, help_text="Requires 2cm padding on all sides")
```

### 2. Box Selection Algorithm & Dimension Calculations
The requirement specifies "2 cm padding on every side". This mathematically means increasing the item's total length, width, and height by 4 cm each (e.g., Left side + Right side = 4cm). 

Rather than polluting the `select_box` function with hardcoded business rules, I introduced an `ItemModifier` interface. The `select_box` function now routes items through this modifier pipeline first, allowing the core volumetric loop to act strictly on "processed" dimensions. 

**Before:**
```python
def select_box(items_data: List[Dict[str, Any]]) -> Box:
    total_weight = Decimal('0.0')
    total_volume = Decimal('0.0')
    
    for item in items_data:
        quantity = Decimal(item.get('quantity', 1))
        weight = Decimal(item['weight'])
        length = Decimal(item['length'])
        # Calculates strictly based on raw JSON input
```

**After:**
```python
from abc import ABC, abstractmethod

class ItemModifier(ABC):
    """Base interface for applying business rules to items before packing."""
    @abstractmethod
    def apply(self, item: Dict[str, Any]) -> Dict[str, Any]:
        pass

class FragilePaddingModifier(ItemModifier):
    """Adds 2cm padding on all sides (4cm total per dimension) for fragile items."""
    def apply(self, item: Dict[str, Any]) -> Dict[str, Any]:
        if item.get('is_fragile', False):
            # Create a copy to prevent mutating the original input reference
            modified_item = item.copy()
            padding = Decimal('4.0')
            modified_item['length'] = Decimal(modified_item['length']) + padding
            modified_item['width'] = Decimal(modified_item['width']) + padding
            modified_item['height'] = Decimal(modified_item['height']) + padding
            return modified_item
        return item

def apply_modifiers(items_data: List[Dict[str, Any]], modifiers: List[ItemModifier]) -> List[Dict[str, Any]]:
    return [mod.apply(item) for item in items_data for mod in modifiers]

def select_box(items_data: List[Dict[str, Any]]) -> Box:
    # 1. Apply rules (OCP pattern)
    modifiers = [FragilePaddingModifier()]
    processed_items = apply_modifiers(items_data, modifiers)

    total_weight = Decimal('0.0')
    total_volume = Decimal('0.0')
    
    # 2. Iterate using processed_items
    for item in processed_items:
        # Calculates based on modified dimensions
        ...
```

### 3. API Endpoints and Validation
The POST API accepts a list of items as a JSON array. Our validation implicitly checks for the `"is_fragile"` boolean flag. Because we use `.get('is_fragile', False)` during deserialization, legacy clients omitting this key will naturally receive a `False` default, preventing breaking API changes. 

## Future Extensibility 

The primary architectural decision in my solution was to introduce the `ItemModifier` interface, strongly aligning with the **Open/Closed Principle (SOLID)**. The core `select_box` algorithm is now closed for modification but open for extension.

Should the business requirements evolve to require:
* **Glass Products:** We can introduce a `GlassOrientationModifier` ensuring glass products only fit upright.
* **Heavy Products:** We can create a `HeavyReinforcementModifier` that adds extra weight to account for heavy-duty reinforcement cardboard.
* **Insulated Packaging:** A `ColdStorageModifier` can add thick insulation layers to dimensions.
* **Custom Rules:** Any specific edge case just requires creating a new class extending `ItemModifier` and appending it to the `modifiers` list in `select_box`, ensuring zero regression risk to the base algorithm.

## Testing and Validation

To validate the safety and accuracy of the change, I wrote boundary tests ensuring both non-fragile and fragile workflows succeed:

* **Happy Path (Legacy):** Confirmed existing test suites evaluating non-fragile standard products continue to fit into the smallest, cheapest appropriate boxes.
* **Padding Shift Test:** I wrote a `test_fragile_padding` scenario. A 9x9x9 object perfectly fits a 10x10x10 Small Box. However, passing `"is_fragile": true` evaluates the object internally as 13x13x13. I successfully verified the unit test correctly rejected the Small Box and upgraded the recommendation to a Medium Box.
* **Weight Integrity:** Ensured that the volumetric inflation did not mistakenly artificially inflate the product's kilogram weight during evaluation.

## Conclusion

By introducing a modular rule-based interceptor pattern, the AI-Assisted Box Selection System now perfectly supports 2 cm padding for fragile objects. The solution is highly scalable, inherently backward compatible, completely tested, and structured optimally for whatever logistical constraints the business defines next.
