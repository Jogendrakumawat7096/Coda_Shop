from django.urls import path
from . import views

urlpatterns = [


    path('', views.index, name="index"),
    path('product/<str:cat>/',views.product,name="product"),   
    path('shoping-cart/',views.shoping_cart,name="shoping-cart"),
    path('product-detail/',views.product_detail,name="product-detail"),
    path('blog/',views.blog,name="blog"),    
    path('about/',views.about,name="about"),
    path('contact/',views.contact,name="contact"),
    path('login/',views.login,name="login"),
    path('signup/',views.signup,name="signup"),
    path('forgot-password/',views.forgot_password,name="forgot-password"),
    path('verify-otp/',views.verify_otp,name="verify-otp"),
    path('new-password/',views.new_password,name="new-password"),
    path('logout/',views.logout,name="logout"),
    path('update-profile/',views.update_profile,name="update-profile"),
    path('update_data/',views.update_data,name="update_data"),
    path('change-password/',views.change_password,name="change-password"),
    path('seller-index/',views.seller_index,name="seller-index"),
    path('seller-add-product/',views.seller_add_product,name="seller-add-product"),
    path('seller-view-product/',views.seller_view_product,name="seller-view-product"),
    path('seller-product-detail/<int:pk>/',views.seller_product_detail,name="seller-product-detail"),
    path('seller-edit-product/<int:pk>/',views.seller_edit_product,name="seller-edit-product"),
    path('seller-product-delete/<int:pk>/',views.seller_product_delete,name="seller-product-delete"),
    path('product-detail/<int:pk>/',views.product_detail,name="product-detail"),
    path('add-to-cart/<int:pk>/',views.add_to_cart,name="add-to-cart"),
    path('add-to-whishlist/<int:pk>/',views.add_to_whishlist,name="add-to-whishlist"), 
    path('whishlist/',views.whishlist,name="whishlist"),
    path('remove-whishlist/<int:pk>/',views.remove_whishlist,name="remove-whishlist"),  
    path('shoping-cart/',views.shoping_cart,name="shoping-cart"),
    path('cart-qty/<int:pk>/', views.cart_qty, name='cart-qty'),
    path('cart-qty-minus/<int:pk>/', views.cart_qty_minus, name='cart-qty-minus'),
    path('remove-cart/<int:pk>/', views.remove_cart, name='remove-cart'),
    path('create-checkout-session/', views.create_checkout_session, name='payment'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel'),
    path('customer-order/', views.customer_order, name='customer-order'),
    path('customer-cancel-order/<int:pk>/', views.customer_cancel_order, name='customer-cancel-order'),
    path('seller-view-order/',views.seller_view_order,name='seller-view-order'),
    path('seller-cancel-order/<int:pk>/',views.seller_cancel_order,name='seller-cancel-order'),
    path('seller-accept-order/<int:pk>/',views.seller_accept_order,name='seller-accept-order'),
    
    
    
    
    
    
]
