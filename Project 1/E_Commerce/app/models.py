from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField

class User(AbstractUser):
    userRole = models.CharField(max_length=3, null=True)

# Create your models here.
class slider(models.Model):
    DISCOUNT_DEAL = (
        ('HOT DEALS','HOT DEALS'),
        ('New Arrivals', 'New Arrivals'),
    )


    Image = models.ImageField(upload_to='media/slider_imgs')
    Discount_Deal = models.CharField(choices=DISCOUNT_DEAL,max_length=100)
    SALE = models.IntegerField()
    Brand_Name = models.CharField(max_length=200)
    Discount = models.IntegerField()
    Link = models.CharField(max_length=200)

    def __str__(self):
        return self.Brand_Name
 
class Main_Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    # main_category = models.ForeignKey(Main_Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)


    # def __str__(self):
        # return self.name    + " -- " + self.main_category.name

class Sub_Category(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.category.main_category.name + " -- " + self.category.name + " -- " + self.name

# class Section(models.Model):
    # name = models.CharField(max_length=100, null=True, blank=True)

    # def __str__(self):
        # return self.name

class Product(models.Model):
    owner_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    total_quantity = models.IntegerField(null=True)
    Availability = models.IntegerField(null=True)
    featured_image = models.ImageField(upload_to='featured_image', null=True)
    product_name = models.CharField(max_length=100)
    price = models.IntegerField(null=True)
    Discount = models.IntegerField(null=True)
    Product_information = RichTextField(null=True)
    model_Name = models.CharField(max_length=100)
    Categories = models.ForeignKey(Category,on_delete=models.CASCADE)
    #Tags = models.CharField(max_length=100)
    Description = RichTextField(null=True)
    is_authenticated = models.BooleanField(default=True)
    #section = models.ForeignKey(Section,on_delete=models.DO_NOTHING,null=True)

    def __str__(self):
        return self.product_name

class Product_Image(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    Image_url = models.ImageField(upload_to='products', null=True)
    

class Additional_Information(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.CharField(max_length=100)
    detail = models.CharField(max_length=100)

    