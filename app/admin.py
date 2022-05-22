from django.contrib import admin
from app.models import Warehouse, InventoryItem
from mapbox_location_field.admin import MapAdmin  

# Register models to admin user
admin.site.register(Warehouse, MapAdmin)
admin.site.register(InventoryItem)
