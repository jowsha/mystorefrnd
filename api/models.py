from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.

class Products(models.Model):
    name=models.CharField(max_length=200,null=True,blank=True)
    description=models.CharField(max_length=200,null=True,blank=True)
    category=models.CharField(max_length=200,null=True,blank=True)
    price=models.PositiveIntegerField(null=True,blank=True)
    image=models.ImageField(upload_to="images",null=True,blank=True)
    def __str__(self):
        return self.name

class Review(models.Model):
    review=models.CharField(max_length=200)
    product_name=models.ForeignKey(Products,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    rating=models.PositiveIntegerField(validators=[MinValueValidator(1),MaxValueValidator(5)])

class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Products,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)

# localhost:8000/products/3/review