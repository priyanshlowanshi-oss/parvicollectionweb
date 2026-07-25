from django.contrib.auth import views as auth_views

"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index , name='index'),
    path('collection-all/', views.collection_all, name='collection_all'), 
    path('editorial/', views.editorial_view, name='editorial'),
    path('editorial/<int:pk>/', views.editorial_detail, name='editorial_detail'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    # यह लाइन जोड़ते ही editorial_detail का एरर भी चला जाएगा
    path('editorial/<int:pk>/', views.editorial_detail, name='editorieditorial_detail'),
    path('add-to-bag/', views.add_to_bag, name='add_to_bag'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('login/', views.login_view, name='login_view'),
    path('register/', views.register_view, name='register_view'),
    path('logout/', views.logout_view, name='logout_view'),
    path('login-with-otp/', views.send_otp_view, name='send_otp_view'), 
    path('verify-otp/', views.verify_otp_view, name='verify_otp_view'),
    path('checkout_view/', views.checkout_view, name='checkout_view'),
    # इसे अपनी urls.py के urlpatterns के अंदर सबसे नीचे जोड़ें
    path('my-orders/', views.my_orders_view, name='my_orders'),
    # इसे अपनी urls.py के urlpatterns के अंदर सबसे नीचे जोड़ें
    path('search/', views.search_view, name='search_product'),
    # इसे अपनी urls.py के urlpatterns के अंदर सबसे नीचे जोड़ें
    path('about/', views.about_view, name='about_page'),
    




        # 1. ईमेल डालने का पेज
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    # 2. ईमेल भेजने के बाद का सक्सेस पेज
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    # 3. ईमेल में आए गुप्त लिंक पर क्लिक करने के बाद नया पासवर्ड सेट करने का पेज
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    # 4. पासवर्ड पूरी तरह बदलने के बाद का फाइनल पेज
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),






    



]
