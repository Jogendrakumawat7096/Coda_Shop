from django.contrib import admin
from .models import User,Whishlist,Product,Cart,Coupon,Order,Contact

# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Whishlist)
admin.site.register(Cart)
admin.site.register(Coupon)
admin.site.register(Order)
admin.site.register(Contact)

