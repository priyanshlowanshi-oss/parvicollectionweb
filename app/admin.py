from django.contrib import admin
# स्टार (*) इम्पोर्ट का उपयोग करके सभी मॉडल्स को एक साथ बुला लिया
from .models import *

# ==========================================
# 1. 📸 प्रोडक्ट गैलरी इनलाइन सेटअप
# ==========================================
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # एडमिन पैनल में हमेशा 3 खाली फ़ोटो अपलोड करने के बॉक्स दिखेंगे

# ==========================================
# 2. 👗 मुख्य प्रोडक्ट एडमिन रजिस्ट्रेशन
# ==========================================
# यहाँ @admin.register लगाना ज़रूरी है ताकि नीचे का इनलाइन बॉक्स एक्टिवेट हो सके
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]  # प्रोडक्ट पेज के अंदर ही गैलरी खुल जाएगी


# ==========================================
# 3. बाकी बचे हुए सभी साधारण मॉडल्स का रजिस्ट्रेशन
# ==========================================
# (नोट: यहाँ से सादा वाला 'Product' पूरी तरह हटा दिया है ताकि एरर न आए)
admin.site.register(EditorialBanner)
admin.site.register(EditorialStory)
admin.site.register(Category)
admin.site.register(CartItem)
admin.site.register(UserOTP)
admin.site.register(Order)
admin.site.register(PaymentSetting) # पेमेंट सेटिंग्स भी जोड़ दी
