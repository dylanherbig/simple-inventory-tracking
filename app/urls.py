from django.urls import path, include


from . import views



app_name = 'app'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'), 
    path('create-warehouse/', views.CreateWarehouseView.as_view(), name="create-warehouse"),
    path('create-inventory-item/', views.CreateInventoryView.as_view(), name="create-inventory"),
    path('get/ajax/warehouse', views.GetWarehouse, name="get-warehouse"),
    path('detail/<int:pk>/', views.DetailWarehouseView.as_view(), name="detail"),
    path('change-inventory/<int:pk>/', views.ChangeInventory, name="change-inventory"),
    path('delete-inventory/<int:pk>/', views.DeleteInventory, name="delete-inventory"),
    path('delete-warehouse/<int:pk>', views.DeleteWarehouse, name="delete-warehouse"),
    path('delete-warehouse/verify/<int:pk>', views.DeleteWarehouseVerify.as_view(), name="delete-warehouse-verify"),
]