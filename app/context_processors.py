from .models import CartItem

def cart_count(request):
    if not request.session.session_key:
        request.session.create()
    
    session_key = request.session.session_key
    # यूजर के सारे आइटम्स की कुल क्वांटिटी गिनें
    items = CartItem.objects.filter(session_key=session_key)
    total_items = sum(item.quantity for item in items)
    
    return {'cart_total_items': total_items}
