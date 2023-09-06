from django.db import models

#Vendors 
class Vendor(models.Model):
    full_name = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='vendor/')
    address = models.TextField()
    phone_number = models.CharField(max_length=12)
    status = models.BooleanField(default=False)
    
    class Meta:
       verbose_name_plural = '1. Vendors'
    
    def __str__(self):
        return self.full_name
    
#Unit 
class Unit(models.Model):
    title = models.CharField(max_length=50)
    short_name = models.CharField(max_length=50)
    
    class Meta:
       verbose_name_plural = '2. Units'
    
    def __str__(self):
        return self.title
    
#Product 
class Product(models.Model):
    title = models.CharField(max_length=50)
    detail = models.TextField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='product/')
    
    class Meta:
       verbose_name_plural = '3. Products'
    
    def __str__(self):
        return self.title
    
#Purchase 
class Purchase(models.Model):
   product = models.ForeignKey(Product, on_delete=models.CASCADE)
   vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
   qty = models.FloatField()
   price = models.FloatField()
   total_amount = models.FloatField()
   purchase_date = models.DateTimeField(auto_now_add=True)
   
   class Meta:
       verbose_name_plural = '4. Purchases'
       
   def save(self, *args, **kwargs):
        self.total_amount = self.qty * self.price
        super(Purchase, self).save(*args, **kwargs)
        
        #Inventory Effect
        inventory = Inventory.objects.filter(product = self.product).order_by('-id').first()
        if inventory:
            totalBal = inventory.total_balance_qty + self.qty
        else:
            totalBal = self.qty
        
        Inventory.objects.create(
            product  = self.product,
            purchase = self,
            sale = None,
            purchase_qty = self.qty,
            sale_qty = None,
            total_balance_qty = totalBal
        )
        
   def __str__(self):
        return self.product
    

#Customer    
class Customer(models.Model):
    customer_name = models.CharField(max_length=50,blank=True)
    customer_mobile = models.CharField(max_length=12,default=None)
    customer_address = models.TextField(default=None)
    
    class Meta:
        verbose_name_plural='7. Customers'
        
    def __str__(self):
        return self.customer_name
    
#Sale 
class Sale(models.Model):
   product = models.ForeignKey(Product, on_delete=models.CASCADE)
   customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
   qty = models.FloatField()
   price = models.FloatField()
   total_amount = models.FloatField(editable=False)
   sale_date = models.DateTimeField(auto_now_add=True)
   
   class Meta:
       verbose_name_plural = '5. Sales'
       
   def save(self, *args, **kwargs):
        self.total_amount = self.qty * self.price
        super(Sale, self).save(*args, **kwargs)
        
        #Inventory Effect
        inventory = Inventory.objects.filter(product = self.product).order_by('-id').first()
        if inventory:
            totalBal = inventory.total_balance_qty - self.qty
        
        Inventory.objects.create(
            product  = self.product,
            purchase = None,    
            sale = self,
            purchase_qty = None,
            sale_qty = self.qty,
            total_balance_qty = totalBal
        )
        
   def __str__(self):
        return self.product
       
#Inventory 
class Inventory(models.Model):
   product = models.ForeignKey(Product, on_delete=models.CASCADE)
   purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, default = 0, null = True)
   sale = models.ForeignKey(Sale, on_delete=models.CASCADE, default = 0, null = True)
   purchase_qty = models.FloatField(default = 0, null = True )
   sale_qty = models.FloatField(default = 0, null = True )
   total_balance_qty = models.FloatField()
   
   class Meta:
        verbose_name_plural = '6. Inventory'
        
   def product_unit(self):
        return self.product.unit.title

   def purchase_date(self):
       if self.purchase:
           return self.purchase.purchase_date 
       
   def sale_date(self):
       if self.sale:
           return self.sale.sale_date