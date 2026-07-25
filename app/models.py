from django.db import models
# Cloudinary फ़ील्ड को इम्पोर्ट किया
from cloudinary.models import CloudinaryField 

# ==========================================
# 1. Category मॉडल
# ==========================================
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Collection Name")
    slug = models.SlugField(unique=True) 

    def __str__(self):
        return self.name


# ==========================================
# 2. EditorialBanner मॉडल
# ==========================================
class EditorialBanner(models.Model):
    title = models.CharField(max_length=200, default="Dressed in Silence.") 
    subtitle = models.CharField(max_length=200, default="SUMMER - AUTUMN 2025") 
    product_details = models.CharField(max_length=200, default="Draped Jersey Set - ₹ 420") 
    image = CloudinaryField('image', folder='editorial_banners/') 
    button_link = models.CharField(max_length=500, default="#") 
    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return self.title


# ==========================================
# 3. Product मॉडल (यहाँ सुधार किया है)
# ==========================================
class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # ImageField हटाकर CloudinaryField लगा दिया
    image = CloudinaryField('image', folder='products/') 
    colors = models.CharField(max_length=100, default="Ivory / Blush", help_text="जैसे: Black / White")
    
    is_new_arrival = models.BooleanField(default=False)
    tag = models.CharField(max_length=50, blank=True, null=True, help_text="जैसे: SIGNATURE")

    def __str__(self):
        return self.name


# ==========================================
# 4. EditorialStory मॉडल (यहाँ भी सुधार किया है)
# ==========================================
class EditorialStory(models.Model):
    CATEGORY_CHOICES = [
        ('lookbook', 'LOOKBOOK'),
        ('essay', 'ESSAY'),
        ('process', 'PROCESS'),
        ('archive', 'ARCHIVE'),
    ]
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='lookbook')
    title = models.CharField(max_length=200, default="In Full Bloom") 
    tagline = models.CharField(max_length=300, default="A study of softness in the age of noise.") 
    content = models.TextField() 
    
    # ImageField हटाकर CloudinaryField लगा दिया
    image = CloudinaryField('image', folder='editorial_stories/') 
    
    issue_number = models.CharField(max_length=100, default="ISSUE 07 — 03 2026") 
    date_published = models.CharField(max_length=100, default="June 2026") 
    read_time = models.CharField(max_length=50, default="5 min read") 
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    editorial_quote = models.CharField(
        max_length=500, 
        default="The quietest clothes are often the loudest statements."
    )
    shop_look_link = models.CharField(max_length=500, default="/collection-all/")

    def __str__(self):
        return self.title




# इसे models.py में सबसे नीचे जोड़ें
class CartItem(models.Model):
    # session_key के जरिए हम बिना लॉगिन किए भी यूजर का सामान याद रख सकते हैं
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)

    session_key = models.CharField(max_length=40, null=True, blank=True)
    
    # कौन सा कपड़ा/प्रोडक्ट जुड़ा है
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    # यूजर ने कौन सा साइज चुना (XS, S, M, L, XL)
    size = models.CharField(max_length=10, default="S")
    
    # कपड़े की मात्रा
    quantity = models.PositiveIntegerField(default=1)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} ({self.size}) x {self.quantity}"
    

# इसे models.py में सबसे ऊपर इम्पोर्ट करें
from django.contrib.auth.models import User

# इसे models.py में सबसे नीचे पेस्ट करें
class UserOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        # OTP सिर्फ 5 मिनट के लिए वैलिड रहेगा
        from django.utils import timezone
        return (timezone.now() - self.created_at).total_seconds() < 300






# ==========================================
# 5. मुख्य ORDER मॉडल (पेमेंट मोड और ट्रांजैक्शन आईडी के साथ)
# ==========================================
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Packed', 'Packed'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]
    
    PAYMENT_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('ONLINE', 'Online QR Payment'),
    ]
    
    # यह ऑर्डर किस यूजर का है, उससे लिंक किया
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    # ग्राहक का शिपिंग डेटाबेस (Address Info)
    full_name = models.CharField(max_length=200, verbose_name="Full Name")
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number")
    address_line_1 = models.CharField(max_length=300, verbose_name="Address Line 1")
    address_line_2 = models.CharField(max_length=300, null=True, blank=True, verbose_name="Address Line 2 (Optional)")
    city = models.CharField(max_length=100, verbose_name="City")
    state = models.CharField(max_length=100, verbose_name="State")
    pincode = models.CharField(max_length=10, verbose_name="Pincode")
    
    # बिल और पेमेंट की पूरी डिटेल्स (नया कोड शामिल है)
    total_bill = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='COD')
    transaction_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="Transaction ID / UTR")
    is_paid = models.BooleanField(default=False, verbose_name="Payment Confirmed by Admin")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"


# ==========================================
# 6. ORDER ITEM मॉडल (ऑर्डर के अंदर के कपड़ों की लिस्ट)
# ==========================================
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    size = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2) 

    def __str__(self):
        return f"{self.product.name} ({self.size}) x {self.quantity}"




# इसे अपनी models.py फ़ाइल के बिल्कुल नीचे पेस्ट करें
class PaymentSetting(models.Model):
    upi_id = models.CharField(max_length=150, verbose_name="Your UPI ID (@ybl, @okaxis)")
    shop_name = models.CharField(max_length=150, verbose_name="Shop / Merchant Name")

    def __str__(self):
        return f"{self.shop_name} ({self.upi_id})"




# इसे models.py के बिल्कुल नीचे पेस्ट करें
from cloudinary.models import CloudinaryField # सुनिश्चित करें कि यह ऊपर भी इम्पोर्ट हो

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = CloudinaryField('image', folder='product_gallery/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Gallery Image for {self.product.name}"



