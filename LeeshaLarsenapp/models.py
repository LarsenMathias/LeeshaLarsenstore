from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model): 
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    email=models.CharField(max_length=150,null=True)
    name=models.CharField(max_length=150,null=True)
    address=models.TextField(max_length=100,blank=True)
    pincode=models.IntegerField(null=True,blank=True)
    city=models.CharField(max_length=30,null=True,blank=True)
    state=models.CharField(max_length=25,null=True,blank=True)
    def __str__(self) -> str:
        return self.email
class Product(models.Model):
    name=models.CharField(max_length=50)
    description=models.CharField(max_length=300)
    price=models.FloatField()
    photo=models.ImageField(upload_to='Images')
    digital=models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.name
class order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    time=models.DateTimeField(auto_now_add=True)
    transaction_id=models.CharField(max_length=200,null=True)
    def __str__(self) -> str:
        return str(self.id)
class cartitem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE,null=True,blank=True)
    order=models.ForeignKey(order,on_delete=models.CASCADE,null=True,blank=True)
    quanity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)
    
