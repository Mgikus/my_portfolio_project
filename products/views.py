from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, ProductCategory, Banner
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import JsonResponse


def index(request):
    products = Product.objects.all()
    banners = Banner.objects.all().order_by("order")
    return render(
        request, "products/index.html", {"products": products, "banners": banners}
    )


def home_view(request):
    return render(request, "index.html", {"is_home_page": True})


def cart_length(request):
    cart = request.session.get("cart", {})
    return len(cart)


def product_list(request):
    products = Product.objects.all()
    cart_len = cart_length(request)
    return render(
        request,
        "products/products_list.html",
        {"products_list": products, "cart_length": cart_len},
    )


def search_view(request):
    query = request.GET.get("q").lower()
    print(f"Запрос в поиске: {query!r}")
    if query:
        products = tuple(
            product
            for product in Product.objects.all()
            if query in product.name.lower()
        )
        for i, product in enumerate(products):
            print(i + 1, product.name, product.description)
        return render(request, "products/search.html", {"products_list": products})
    else:
        return redirect("product_list")


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    is_liked = str(product.id) in request.session.get("like", {})

    cart = request.session.get("cart", {})
    added = str(product.id) in cart

    return render(
        request,
        "products/product_detail.html",
        {
            "product": product,
            "added": added,
            "is_liked": is_liked,
        },
    )


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get("cart", {})

    if str(product.id) in cart:
        cart[str(product.id)]["quantity"] += 1
    else:
        cart[str(product.id)] = {
            "name": product.name,
            "price": str(product.price),
            "quantity": 1,
            "image": product.image.url,
        }

    request.session["cart"] = cart

    return JsonResponse({"cart_length": len(cart)})


def cart(request):
    cart = request.session.get("cart", {})
    total_price = sum(float(item["price"]) * item["quantity"] for item in cart.values())
    return render(
        request, "products/cart.html", {"cart": cart, "total_price": total_price}
    )


def update_cart(request, product_id, action):
    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        if action == "increase":
            cart[str(product_id)]["quantity"] += 1
        elif action == "decrease":
            if cart[str(product_id)]["quantity"] > 1:
                cart[str(product_id)]["quantity"] -= 1
            else:
                del cart[str(product_id)]

    request.session["cart"] = cart
    return redirect("cart")


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("product_list")
    else:
        form = UserCreationForm()
    return render(request, "products/register.html", {"form": form})


def category_view(request, category_id):
    category = get_object_or_404(ProductCategory, id=category_id)
    products = Product.objects.filter(category=category)
    context = {
        "category": category,
        "products": products,
    }
    return render(request, "products/category.html", context)


def like_view(request):
    like = request.session.get("like", {})
    return render(request, "products/liked.html", {"like": like})


def add_to_like(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    like = request.session.get("like", {})
    product_key = str(product.id)
    response_data = {"is_liked": True}

    if product_key in like:
        del like[product_key]
        response_data["is_liked"] = False
        response_data["message"] = "Товар удален из избранного"
    else:
        like[product_key] = {
            "name": product.name,
            "price": str(product.price),
            "image": product.image.url,
        }
        response_data["message"] = "Товар добавлен в избранное"

    request.session["like"] = like
    request.session.modified = True
    return JsonResponse(response_data)
