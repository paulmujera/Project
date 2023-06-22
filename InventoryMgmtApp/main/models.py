from django.db import models

#Vendors 
class Vendor(models.Model):
    full_name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='vendor/')
    address = models.TextField()
    phone_number = models.CharField(max_length=12)
    status = models.BooleanField(default=False)
    
    def __str__(self):
        return self.full_name
    
#Unit 
class Unit(models.Model):
    title = models.CharField(max_length=50)
    short_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.title
    
#Product 
class Product(models.Model):
    title = models.CharField(max_length=50)
    detail = models.TextField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='product/')
    
    def __str__(self):
        return self.title
    
#Purchase 
class Purchase(models.Model):
   product = models.ForeignKey(Product, on_delete=models.CASCADE)
   vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
   qty = models.FloatField()
   price = models.FloatField()
   total_amount = models.FloatField()
   pur_date = models.DateTimeField(auto_now_add=True)
   
   class Meta:
       verbose_name_plural = 'Purchases'
#Sale 
class Sale(models.Model):
   product = models.ForeignKey(Product, on_delete=models.CASCADE)
   qty = models.FloatField()
   price = models.FloatField()
   total_amount = models.FloatField()
   sale_date = models.DateTimeField(auto_now_add=True)
   
   customer_name = models.CharField(max_length=50,blank=True)
   customer_mobile = models.CharField(max_length=12,default=None)
   customer_address = models.TextField(default=None)
   
   class Meta:
       verbose_name_plural = 'Sales'
       
#Inventory 
class Inventory(models.Model):
   product = models.ForeignKey(Product, on_delete=models.CASCADE)
   purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, default = 0)
   sale = models.ForeignKey(Sale, on_delete=models.CASCADE, default = 0)
   purchase_qty = models.FloatField(default = 0 )
   sale_qty = models.FloatField(default = 0 )
   total_balance_qty = models.FloatField()
   
   class Meta:
       verbose_name_plural = 'Inventory'
