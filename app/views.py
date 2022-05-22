from asyncio.windows_events import NULL
from operator import ge
from urllib import request
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect

from django.views import generic

from .forms import WarehouseForm, InventoryForm
from .models import InventoryItem, Warehouse

from django.http import JsonResponse

class IndexView(generic.ListView):
    template_name = 'app/index.html'
    context_object_name = 'warehouses'

    def get_queryset(self):
        # Return all warehouses 
        return Warehouse.objects.all()

def GetWarehouse(request):
    if is_ajax(request) and request.method == "GET":
        lat = request.GET.get("lat", None)
        lng = request.GET.get("lng", None)

        try:
            coordinates = (abs(float(lng)), abs(float(lat)))
            sum = coordinates[0] + coordinates[1]

            min_diff = 720 # max possible distance between two coordinates
            warehouse = None

            # Iterate through every warehouse and check which absolute difference to point is smallest
            for wh in Warehouse.objects.all():
                temp_coordinates = wh.location
                temp_sum = abs(temp_coordinates[0]) + abs(temp_coordinates[1])

                if abs(temp_sum - sum) < min_diff and abs(temp_sum - sum) < 0.1:
                    min_diff = abs(temp_sum - sum)
                    warehouse = wh

            if isinstance(warehouse, type(None)): # check if click was not on marker
                return JsonResponse({"valid":False}, status = 200)


            inventory_items = InventoryItem.objects.filter(warehouse = warehouse)

            print(inventory_items)
        except Exception:
            return JsonResponse({"valid":False}, status = 200)
        return JsonResponse((list(inventory_items.values('id', 'title', 'amount', 'measurement', 'warehouse')), warehouse.title, warehouse.id), safe = False) 

# Verifies if request is of ajax
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

class CreateWarehouseView(generic.CreateView):
    template_name = 'app/createWarehouse.html'
    form_class = WarehouseForm
    success_url = reverse_lazy('app:index')

class CreateInventoryView(generic.CreateView):
    template_name = 'app/createInventory.html'
    form_class = InventoryForm
    success_url = reverse_lazy('app:index')    

class DetailWarehouseView(generic.DetailView):
    template_name = 'app/detail.html'
    model = Warehouse

# Function to change inventory on request
def ChangeInventory(request, pk):
    
    if request.method == "POST":
        inventory_item = get_object_or_404(InventoryItem, pk=pk) # creates 404 html respond if inventory item does not exist

        # If input is below 1 or the input field is empty, the inventory will be deleted
        if isinstance(request.POST.get("amount", None), type(None)) or int(request.POST.get("amount", None)) < 1 :
            inventory_item.delete()

        InventoryItem.objects.filter(pk=pk).update(amount=int(request.POST.get("amount")))
        
        return redirect('app:detail', pk=inventory_item.warehouse.id)

def DeleteInventory(request, pk):
    
    inventory_item = get_object_or_404(InventoryItem, pk=pk) # creates 404 html respond if inventory item does not exist
    id = inventory_item.warehouse.id # creates 404 html respond if warehouse item does not exist
    inventory_item.delete() # delete inventory item

    return redirect('app:detail', pk=id)

class DeleteWarehouseVerify(generic.DetailView):
    template_name = 'app/deleteWarehouseVerify.html'
    model = Warehouse

def DeleteWarehouse(request, pk):
    
    warehouse = get_object_or_404(Warehouse, pk=pk)

    for item in warehouse.inventory_items.all():
        item.delete()
    
    warehouse.delete()

    return redirect('app:index')
