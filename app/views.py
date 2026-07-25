
import cloudinary
import cloudinary.uploader
import cloudinary.api

# सीधे व्यू लेवल पर क्रेडेंशियल्स एक्टिवेट करना (यह एरर को तुरंत ब्लॉक कर देगा)
cloudinary.config( 
  cloud_name = 'dggvv4dgv', 
  api_key = '536522447941463',       # यहाँ अपनी असली बिना * वाली पूरी API KEY लिखें
  api_secret = 'J-PbE3MM2Od4SRVIBumukQ4vUdg'  # यहाँ अपना असली बिना * वाला पूरा API SECRET लिखें
)

# इसके नीचे आपका पुराना इम्पोर्ट कोड रहेगा:
from django.shortcuts import render, redirect, get_object_or_404
from .models import EditorialBanner, Product, Category, EditorialStory

# ... बाकी का पूरा इंडेक्स, कलेक्शन और एडिटोरियल फ़ंक्शंस नीचे वैसे ही रहेंगे ...



from django.shortcuts import render, redirect, get_object_or_404
from .models import EditorialBanner, Product, Category, EditorialStory

# ==========================================
# 1. होमपेज (Front View / Index Page)
# ==========================================
def index(request):
    # 1. बैनर्स का डेटा निकाला
    banners = EditorialBanner.objects.filter(is_active=True)
    
    # 2. न्यू अराइवल्स के सिर्फ 3 लेटेस्ट प्रोडक्ट्स निकाले
    new_arrivals = Product.objects.filter(is_new_arrival=True).order_by('-id')[:3]
    
    # 3. नया कोड: डेटाबेस से सबसे आखिरी में डाले गए 4 प्रोडक्ट्स निकाले (The Latest Drop के लिए)
    latest_drops = Product.objects.all().order_by('-id')[:4]
    
    context = {
        'banners': banners,
        'new_arrivals': new_arrivals,
        'latest_drops': latest_drops  # इसे कॉन्टेक्स्ट में पास कर दिया
    }
    return render(request, 'index.html', context)

# ==========================================
# 2. ऑल कलेक्शंस पेज (Category Filters)
# ==========================================
def collection_all(request):
    # 1. डेटाबेस से सारे कलेक्शंस (Categories) निकालें ऊपर बटन्स के लिए
    categories = Category.objects.all()
    
    # 2. यूआरएल से category का नाम और new_arrivals का स्टेटस पकड़ें
    category_slug = request.GET.get('category')
    is_new_filter = request.GET.get('new_arrivals')
    
    # सुधार: यहाँ कंडीशन को एकदम मजबूत कर दिया है
    if is_new_filter == 'true' or 'new_arrivals=true' in request.get_full_path():
        # अब यह सिर्फ और सिर्फ वही प्रोडक्ट्स निकालेगा जिन पर एडमिन पैनल में टिक (True) किया गया है
        products = Product.objects.filter(is_new_arrival=True).order_by('-id')
    elif category_slug:
        # अगर किसी खास कैटेगरी/बटन पर क्लिक हुआ है
        products = Product.objects.filter(category__slug=category_slug).order_by('-id')
    else:
        # नॉर्मल ऑल कलेक्शन पेज पर सारे प्रोडक्ट्स दिखाओ
        products = Product.objects.all().order_by('-id')
        
    context = {
        'categories': categories,
        'products': products,
        'selected_category': category_slug,
        'is_new_filter': 'true' if is_new_filter == 'true' else ''
    }
    return render(request, 'collection_all.html', context)

# ==========================================
# 3. एडिटोरियल लिस्ट पेज (Lookbooks & Essays)
# ==========================================
def editorial_view(request):
    selected_filter = request.GET.get('type')
    
    if selected_filter:
        # अगर यूजर ने कोई फिल्टर चुना है (जैसे: ESSAY), तो सारी मैचिंग स्टोरीज दिखाएं
        stories = EditorialStory.objects.filter(category=selected_filter, is_published=True).order_by('-created_at')
        latest_story = None
        past_issues = stories
    else:
        # नॉर्मल पेज पर: सारी पब्लिश स्टोरीज निकालें
        stories = EditorialStory.objects.filter(is_published=True).order_by('-created_at')
        
        # सबसे पहली/नई स्टोरी ऊपर बड़े बैनर के लिए
        latest_story = stories.first() if stories.exists() else None
        
        # पहली स्टोरी को छोड़कर बाकी सब नीचे ग्रिड (Past Issues) के लिए
        past_issues = stories[1:] if stories.count() > 1 else []
        
    context = {
        'latest_story': latest_story,
        'past_issues': past_issues,
        'selected_filter': selected_filter
    }
    return render(request, 'editorial.html', context)


# ==========================================
# 4. एडिटorial डिटेल पेज (सिंगल स्टोरी व्यू)
# ==========================================
# नोट: डुप्लीकेट फंक्शन हटा दिया गया है, यह सिर्फ एक बार रहेगा
def editorial_detail(request, pk):
    story = get_object_or_404(EditorialStory, pk=pk)
    return render(request, 'editorial_detail.html', {'story': story})


# ==========================================
# ==========================================
# 5. प्रोडक्ट डिटेल पेज (मल्टी-इमेज गैलरी के साथ)
# ==========================================
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # 🎯 नया कोड: इस प्रोडक्ट से जुड़ी सभी एक्स्ट्रा गैलरी फोटोज को ढूंढना
    gallery_images = product.images.all() 
    
    context = {
        'product': product,
        'gallery_images': gallery_images  # इसे कॉन्टेक्स्ट में पास कर दिया
    }
    return render(request, 'product_detail.html', context)



from django.http import JsonResponse
from .models import Product, CartItem


def add_to_bag(request):
    if request.method == "POST":
        if not request.session.session_key:
            request.session.create()
            
        session_key = request.session.session_key
        product_id = request.POST.get('product_id')
        size = request.POST.get('size', 'S') # डिफ़ॉल्ट साइज S रहेगा
        
        product = get_object_or_404(Product, id=product_id)
        
        # चेक करें कि क्या यह सामान इसी साइज में पहले से कार्ट में है?
        cart_item, created = CartItem.objects.get_or_create(
            session_key=session_key,
            product=product,
            size=size
        )
        
        if not created:
            # अगर पहले से है, तो सिर्फ गिनती 1 बढ़ा दो
            cart_item.quantity += 1
            cart_item.save()
            
        return redirect(request.META.get('HTTP_REFERER', 'index'))






# इसे views.py में सबसे नीचे जोड़ें
# views.py ke bilkul neeche is function ko jodein

from django.db.models import Sum
def cart_view(request):
    # Sabse pehle sunishchit karein ki session bana ho
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    # Agar user login hai, toh uske account ke items dikhao
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        # BACKUP: Agar naye account mein items abhi transfer nahi hue hain, toh session se uthao
        if not cart_items.exists():
            cart_items = CartItem.objects.filter(session_key=session_key)
    else:
        # Agar user login nahi hai, toh guest session ke items dikhao
        cart_items = CartItem.objects.filter(session_key=session_key)
        
    subtotal = sum(item.total_price() for item in cart_items)
    
    # Kapdo ki kul quantity ka jod nikaalein (Counter ke liye)
    total_items = sum(item.quantity for item in cart_items)
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'total_items': total_items
    })





# सामान को बैग से हटाने (Delete) का फंक्शन
from django.shortcuts import get_object_or_404, redirect
from .models import CartItem

def remove_from_cart(request, item_id):
    if request.method == "POST":
        # Direct database se is item ko pakdo, bina ye soche ki user login hai ya nahi
        item = get_object_or_404(CartItem, id=item_id)
        item.delete()
        
    return redirect('cart_view')







from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages

# 1. ग्राहक रजिस्ट्रेशन व्यू
import random

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

import random
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login

def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        otp_entered = request.POST.get('otp')

        # 🔐 स्टेज 2: ग्राहक ने OTP डाला और 'CREATE ACCOUNT' दबाया (Isko pehle check karenge)
        if otp_entered:
            s_name = request.session.get('signup_name')
            s_email = request.session.get('signup_email')
            s_password = request.session.get('signup_password')
            s_otp = request.session.get('signup_otp')
            
            if s_otp and str(s_otp) == str(otp_entered).strip():
                # User Create Karein
                user = User.objects.create_user(username=s_email, email=s_email, password=s_password)
                user.first_name = s_name
                user.save()
                
                login(request, user)
                
                # Session clear karein
                keys_to_delete = ['signup_name', 'signup_email', 'signup_password', 'signup_otp']
                for key in keys_to_delete:
                    request.session.pop(key, None)
                    
                return redirect('index')
            else:
                return render(request, 'register.html', {
                    'first_name': s_name, 
                    'email': s_email, 
                    'password': s_password, 
                    'otp_sent': True, 
                    'error': 'गलत OTP, कृपया दोबारा सही OTP भरें!'
                })

        # 🛑 स्टेज 1: ग्राहक ने ईमेल भरा और पहली बार 'SEND OTP' दबाया
        elif email:
            if User.objects.filter(email=email).exists():
                return render(request, 'register.html', {'error': "इस ईमेल से अकाउंट पहले से बना हुआ है। लॉगिन करें।"})

            generated_otp = str(random.randint(100000, 999999))
            request.session['signup_otp'] = generated_otp

            # Email Send Block with Error Catching ✉️
            try:
                send_mail(
                    subject="Parvi Studio - Email Verification OTP",
                    message=f"Hello {first_name},\n\nYour OTP for Parvi Studio registration is: {generated_otp}\n\nThanks,\nParvi Studio",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
            except Exception as e:
                # Agar Google connection fail hoga toh screen par error dikhega
                return render(request, 'register.html', {
                    'first_name': first_name,
                    'email': email,
                    'password': password,
                    'error': f"Email nahi bheja ja saka! Wajah: {str(e)}"
                })

            # Data ko session mein save karein
            request.session['signup_name'] = first_name
            request.session['signup_email'] = email
            request.session['signup_password'] = password
            
            return render(request, 'register.html', {
                'first_name': first_name,
                'email': email,
                'password': password,
                'otp_sent': True
            })

    return render(request, 'register.html')


# 2. ग्राहक लॉगिन व्यू
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "गलत ईमेल या पासवर्ड। कृपया दोबारा जांचें।")
            return redirect('login_view')
            
    return render(request, 'login.html')

# 3. लॉगआउट व्यू
def logout_view(request):
    logout(request)
    return redirect('index')





import random
from .models import UserOTP
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, get_user_model
import random

User = get_user_model()
# settings ya views ke baki imports ke sath sabse upar ise jodein:
from django.views.decorators.csrf import csrf_protect

# =======================================================
# ✉️ 2. OTP भेजने का व्यू (NEXT PARAMETER KO SATH LEKAR CHALEGA)
# =======================================================
@csrf_protect
def send_otp_view(request):
    next_page = request.GET.get('next') or request.POST.get('next') or ''
    
    if request.method == "POST":
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        
        if not user:
            return render(request, 'send_otp.html', {'error': "यह ईमेल हमारे डेटाबेस में पंजीकृत नहीं है।", 'next': next_page})
            
        otp_code = str(random.randint(100000, 999999))
        UserOTP.objects.filter(user=user).delete()
        UserOTP.objects.create(user=user, otp=otp_code)
        
        try:
            send_mail(
                subject="Parvi Studio - Login Verification OTP",
                message=f"Hello,\n\nYour OTP for logging into Parvi Studio is: {otp_code}\n\nThanks,\nParvi Studio",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            return render(request, 'send_otp.html', {'error': f"Email nahi bheja ja saka! Wajah: {str(e)}", 'next': next_page})
        
        request.session['otp_email'] = email
        
        # 💡 Sahi Verify-OTP path par parameter pass karein
        return redirect(f"/verify-otp/?next={next_page}")
        
    return render(request, 'send_otp.html', {'next': next_page})

@csrf_protect
def verify_otp_view(request):
    email = request.session.get('otp_email')
    next_page = request.GET.get('next') or request.POST.get('next') or ''
    
    if not email:
        return redirect(f"/login-with-otp/?next={next_page}")
        
    if request.method == "POST":
        otp_entered = request.POST.get('otp')
        user = get_object_or_404(User, email=email)
        user_otp = UserOTP.objects.filter(user=user).last()
        
        if user_otp and user_otp.otp == str(otp_entered).strip() and user_otp.is_valid():
            
            # 🔥 STEP A: Guest session key save karein
            guest_session_key = request.session.session_key
            
            # Django Login
            login(request, user)
            
            # 🔥 STEP B: GUEST SE USER TAK KAPDE TRANSFER KAREIN
            if guest_session_key:
                CartItem.objects.filter(session_key=guest_session_key).update(user=user)
            
            request.session.pop('otp_email', None)
            user_otp.delete()
            
            # 🔥 STEP C: Agar next_page maujood hai (yaani /checkout_view/), toh wahan redirect karein
            if next_page:
                return redirect(next_page)
                
            return redirect('index')
        else:
            return render(request, 'verify_otp.html', {
                'email': email, 
                'error': "गलत या एक्सपायर्ड OTP। कृपया दोबारा प्रयास करें।",
                'next': next_page
            })
            
    return render(request, 'verify_otp.html', {'email': email, 'next': next_page})



import qrcode
import io
import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CartItem, Order, OrderItem, PaymentSetting

# def checkout_view(request):
#     # 1. सेशन से यूजर की जांच करना (पुराना सुरक्षित तरीका)
#     user_id = request.session.get('user_id')
#     if not user_id:
#         return redirect('login_view') 

#     real_user = get_object_or_404(User, id=user_id)
#     cart_items = CartItem.objects.filter(user=real_user)
    
#     if not cart_items.exists():
#         return redirect('cart_view')
        
#     # 2. बिल और शिपिंग का हिसाब
#     subtotal = sum(item.total_price() for item in cart_items)
#     shipping = 0 if subtotal >= 300 else 15
#     total = float(subtotal + shipping)

#     # 3. 🎯 आपके डेटाबेस (PaymentSetting) से UPI ID और नाम उठाना
#     upi_setting = PaymentSetting.objects.first()
#     if upi_setting:
#         real_upi = upi_setting.upi_id
#         real_shop_name = upi_setting.shop_name 
#     else:
#         # अगर डेटाबेस खाली है तो बैकअप के लिए आपकी @ybl वाली आईडी
#         real_upi = "sadh.vicky@ybl"  
#         real_shop_name = "Parvi Collection"

#     # 4. ⚡ बैकएंड में हवा की रफ्तार से सुरक्षित QR कोड बनाना
#     try:
#         # यहाँ cu=EUR कर दिया है ताकि विदेशी ग्राहकों के लिए भी सही रहे
#         upi_string = f"upi://pay?pa={real_upi}&pn={real_shop_name.replace(' ', '%20')}&mc=0000&mode=02&purpose=00&am={total}&cu=EUR"
        
#         qr = qrcode.QRCode(version=1, box_size=10, border=2)
#         qr.add_data(upi_string)
#         qr.make(fit=True)
#         img = qr.make_image(fill_color="black", back_color="white")

#         # इमेज को बाइट्स में बदलकर सुरक्षित Base64 बनाना
#         buffer = io.BytesIO()
#         img.save(buffer, format="PNG")
#         secure_qr_image = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
#     except Exception as e:
#         print(f"QR Code generation failed: {e}")
#         secure_qr_image = None

#     # 5. 📥 फॉर्म सबमिट होने पर डेटा सहेजना (POST Request)
#     if request.method == 'POST':
#         full_name = request.POST.get('full_name')
#         phone_number = request.POST.get('phone')
#         address_1 = request.POST.get('address_1')
#         address_2 = request.POST.get('address_2')
#         city = request.POST.get('city')
#         state = request.POST.get('state')
#         pincode = request.POST.get('pincode')
#         payment_method = request.POST.get('payment_method')
#         transaction_id = request.POST.get('transaction_id')

#         # Order table में पूरा डेटा सहेजना
#         order = Order.objects.create(
#             user=real_user,
#             full_name=full_name,
#             phone_number=phone_number,
#             address_line_1=address_1,
#             address_line_2=address_2,
#             city=city,
#             state=state,
#             pincode=pincode,
#             total_bill=total,
#             payment_method=payment_method,
#             transaction_id=transaction_id if payment_method == 'ONLINE' else '',
#             is_paid=True if payment_method == 'COD' else False # COD पर तुरंत हां, ऑनलाइन पर एडमिन की जांच बाकी
#         )
        
#         # कार्ट के सामान को परमानेंट आर्डर हिस्ट्री में ट्रांसफर करना
#         for item in cart_items:
#             OrderItem.objects.create(
#                 order=order,
#                 product=item.product,
#                 size=item.size,
#                 quantity=item.quantity,
#                 price=item.product.price
#             )
        
#         cart_items.delete() # ऑर्डर पक्का होते ही झोला खाली
        
#         # सीधे आपके नए कंडीशनल order_success पेज पर भेजना
#         return render(request, 'order_success.html', {'order': order})

#     context = {
#         'cart_items': cart_items,
#         'subtotal': subtotal,
#         'shipping': shipping,
#         'total': total,
#         'secure_qr_image': secure_qr_image, # फ्रंटएंड के लिए एकदम सुरक्षित इमेज स्ट्रिंग
#     }
#     return render(request, 'checkout.html', context)


import io
import base64
import qrcode
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CartItem, Order, OrderItem, PaymentSetting


import random
import io
import base64
import qrcode
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, get_user_model
from django.urls import reverse # 💡 URL path automatic nikaalne ke liye import
from django.views.decorators.csrf import csrf_protect # CSRF security ke liye
from .models import CartItem, UserOTP, PaymentSetting
# settings ya views ke baki imports ke sath sabse upar ise jodein:
from django.views.decorators.csrf import csrf_protect




# =======================================================
# 🛍️ 1. CHECKOUT VIEW (YAHAN SE LOGIN PAR BHEJA JAYEGA)
# =======================================================
User = get_user_model()

# =======================================================
# 🛍️ 1. CHECKOUT VIEW (RAASTA: /checkout_view/)
# =======================================================
from django.urls import reverse # Agar upar import na ho toh kar lein

def checkout_view(request):
    # 💡 Agar customer login nahi hai, toh reverse() ka use karke ekdum sahi path nikaalein
    if not request.user.is_authenticated:
        sahi_checkout_path = reverse('checkout_view') # Yeh automatic '/checkout_view/' nikaal lega
        return redirect(f"/login-with-otp/?next={sahi_checkout_path}") 

    real_user = request.user
    
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    
    # Authenticated user ke items check karein
    cart_items = CartItem.objects.filter(user=real_user)
    
    if not cart_items.exists():
        return redirect('cart_view')
        
    subtotal = sum(item.total_price() for item in cart_items)
    total_items = sum(item.quantity for item in cart_items)

    # 🛑 स्टेज 1: ग्राहक ने पहली बार एड्रेस फॉर्म भरा और सबमिट किया
    if request.method == 'POST' and 'address_submit' in request.POST:
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address_1 = request.POST.get('address_1')
        address_2 = request.POST.get('address_2')
        city = request.POST.get('city', '').strip()
        state = request.POST.get('state', '').strip()
        pincode = request.POST.get('pincode')

        city_lower = city.lower()
        state_lower = state.lower()
        base_shipping_inr = 40

        north_east_states = ['assam', 'meghalaya', 'tripura', 'mizoram', 'manipur', 'nagaland', 'arunachal pradesh', 'sikkim', 'jammu', 'kashmir', 'andaman', 'nicobar']

        if city_lower == 'bhopal':
            base_shipping_inr = 40
        elif state_lower == 'madhya pradesh' or state_lower == 'mp':
            base_shipping_inr = 80
        elif any(ne_state in state_lower for ne_state in north_east_states):
            base_shipping_inr = 160
        else:
            base_shipping_inr = 110

        if total_items > 2:
            extra_items = total_items - 2
            shipping_inr = base_shipping_inr + (extra_items * 25)
        else:
            shipping_inr = base_shipping_inr

        total = float(subtotal) + float(shipping_inr)

        request.session['checkout_data'] = {
            'full_name': full_name, 'phone': phone, 'address_1': address_1,
            'address_2': address_2, 'city': city, 'state': state, 'pincode': pincode,
            'shipping': shipping_inr, 'total': total
        }

        upi_setting = PaymentSetting.objects.first()
        real_upi = upi_setting.upi_id if upi_setting else "sadh.vicky@ybl"
        real_shop_name = upi_setting.shop_name if upi_setting else "Parvi Collection"

        try:
            upi_string = f"upi://pay?pa={real_upi}&pn={real_shop_name.replace(' ', '%20')}&mc=0000&mode=02&purpose=00&am={total}&cu=INR"
            qr = qrcode.QRCode(version=1, box_size=10, border=2)
            qr.add_data(upi_string)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            secure_qr_image = f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
        except Exception as e:
            secure_qr_image = None

        return render(request, 'payment_step.html', {
            'cart_items': cart_items, 'subtotal': subtotal, 'shipping': shipping_inr,
            'total': total, 'secure_qr_image': secure_qr_image
        })
        
    return render(request, 'checkout.html', {'cart_items': cart_items, 'subtotal': subtotal})




# ==========================================
# 🛒 ग्राहक का ऑर्डर हिस्ट्री व्यू (MY ORDERS - 100% FIXED)
# ==========================================
def my_orders_view(request):
    if not request.user.is_authenticated:
        return redirect('login_view')

    real_user = request.user
    
    # 🎯 सुधार: उलझा हुआ लॉजिक हटाकर सीधे साफ़ शब्दों में इस यूज़र के ऑर्डर्स निकाले
    # इससे नए ऑर्डर्स हमेशा लिस्ट में सबसे ऊपर दिखाई देंगे (-created_at की वजह से)
    user_orders = Order.objects.filter(user=real_user).order_by('-created_at')

    context = {
        'orders': user_orders,
        'cart_total_items': sum(item.quantity for item in CartItem.objects.filter(session_key=request.session.session_key)) if request.session.session_key else 0
    }
    return render(request, 'my_orders.html', context)




from django.db.models import Q # 👈 चेक कर लें कि यह ऊपर इम्पोर्ट है या नहीं, नहीं तो सबसे ऊपर लिख दें

# ==========================================
# 🔍 पारवी स्टूडियो लाइव सर्च इंजन VIEW
# ==========================================
# ==========================================
# 🔍 पारवी स्टूडियो लाइव सर्च इंजन VIEW (100% FIXED)
# ==========================================
def search_view(request):
    query = request.GET.get('q', '').strip()
    results = Product.objects.none()

    if query:
        # 🎯 सुधार: 'description' हटा दिया है, अब यह सिर्फ नाम (name) और टैग (tag) में ढूंढेगा ताकि एरर न आए
        results = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(tag__icontains=query)
        ).distinct()

    context = {
        'query': query,
        'products': results,
        'cart_total_items': sum(item.quantity for item in CartItem.objects.filter(session_key=request.session.session_key)) if request.session.session_key else 0
    }
    return render(request, 'search_results.html', context)





# views.py के product_detail व्यू को इससे बदलें
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    gallery_images = product.images.all() 
    
    # 🎯 नया लॉजिक: डेटाबेस से इस प्रोडक्ट को छोड़कर कोई भी 4 अन्य कपड़े रैंडमली (order_by('?')) उठाना
    recommended_products = Product.objects.exclude(pk=pk).order_by('?')[:4]
    
    context = {
        'product': product,
        'gallery_images': gallery_images,
        'recommended_products': recommended_products, # इसे कॉन्टेक्स्ट में भेज दिया
        'cart_total_items': sum(item.quantity for item in CartItem.objects.filter(session_key=request.session.session_key)) if request.session.session_key else 0
    }
    return render(request, 'product_detail.html', context)




# ==========================================
# 🏛️ पारवी स्टूडियो 'ABOUT US' कहानी VIEW
# ==========================================
def about_view(request):
    context = {
        # कार्ट काउंट को ज़िंदा रखा ताकि हेडर में झोले का नंबर सही दिखे
        'cart_total_items': sum(item.quantity for item in CartItem.objects.filter(session_key=request.session.session_key)) if request.session.session_key else 0
    }
    return render(request, 'about.html', context)
