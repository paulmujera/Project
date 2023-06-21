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