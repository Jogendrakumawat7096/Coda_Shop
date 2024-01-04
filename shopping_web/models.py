from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    mobile = models.PositiveBigIntegerField()
    address =models.TextField()
    password = models.CharField(max_length=150)
    image = models.ImageField(upload_to='profile_image/')
    user_type=models.CharField(max_length=100,default="buyer")

    
    def __str__(self):
        return self.name

class Contact(models.Model):
    email=models.EmailField()
    message=models.TextField()
    
    def __str__(self):
        self.email

class Product(models.Model):
    Category=(
        ("Men","Men"),
        ("Women","Women"),
        ("kids","kids"),
    )
    Brand=(
        ("luvis","luvis"),
        ("Diesel","Diesel"),
        ("polo","polo"),
    )
    Size=(
        ("s","s"),
        ("l","l"),
        ("xl","xl"),
        ("xxl","xxl"),
    )
    seller=models.ForeignKey(User,on_delete=models.CASCADE)
    product_name=models.CharField(max_length=150)
    product_price=models.PositiveIntegerField()
    product_category=models.CharField(max_length=100,choices=Category)
    product_brand=models.CharField(max_length=100,choices=Brand)
    product_size=models.CharField(max_length=100,choices=Size)
    product_desc=models.TextField()
    product_fimage=models.ImageField(upload_to="product_image/")
    product_bimage=models.ImageField(upload_to="product_image/")
    
    def __str__(self):
        return self.seller.name+"-"+self.product_name

class Whishlist(models.Model):
    buyer=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    
    def __str__(self):
        return self.buyer.name+"-"+self.product.product_name
    
class Cart(models.Model):
    buyer=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    product_price=models.PositiveBigIntegerField()
    product_qty=models.PositiveBigIntegerField(default=1)
    total_price=models.PositiveBigIntegerField()
    payment_status=models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.buyer.name+"-"+self.product.product_name
    

class Coupon(models.Model):
    code=models.CharField(max_length=100)
    discount=models.PositiveIntegerField()
    
    def __str__(self):
        return self.code
    

class Order(models.Model):
    buyer=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    product_price=models.PositiveBigIntegerField()
    product_qty=models.PositiveBigIntegerField(default=1)
    total_price=models.PositiveBigIntegerField()
    order_status=models.CharField(max_length=150,default="pending")