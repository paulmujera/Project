from django.contrib import admin
from . import models
admin.site.register(models.Vendor)
admin.site.register(models.Unit)
admin.site.register(models.Product)

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'qty', 'price','total_amount', 'vendor', 'purchase_date']
admin.site.register(models.Purchase,PurchaseAdmin)

admin.site.register(models.Sale)
admin.site.register(models.Inventory)
