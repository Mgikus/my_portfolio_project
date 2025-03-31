from products.models import ProductCategory


def cart_context(request):
    cart = request.session.get("cart", {})
    categories = ProductCategory.objects.all()
    return {
        "cart": cart,
        "cart_length": len(cart),
        "categories": categories,
    }
