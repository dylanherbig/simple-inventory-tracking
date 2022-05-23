from django.db import models 
from mapbox_location_field.models import LocationField

from django.core.validators import MinValueValidator
from django.db import models

# Warehouse
class Warehouse(models.Model):
    location = LocationField(map_attrs={"center": [-77.03, 38.91], "zoom": 9})
    title = models.CharField(max_length=100, blank=False)
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['warehouses'] = Warehouse.objects.all()
        return context

# Inventory item
class InventoryItem(models.Model):
    title = models.CharField(max_length=100, blank=False)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="inventory_items")
    pub_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now_add=True, null=True)

    amount = models.IntegerField(
        default=1,
        validators=[
            MinValueValidator(1)  # minimum value indicator 
        ]
    )
    measurement = models.CharField(max_length=100, blank=False, null=True)

    def __str__(self):
        return self.title


