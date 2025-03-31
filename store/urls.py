"""
URL configuration for store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from products import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path("admin/", admin.site.urls),
    path("products/", views.product_list, name="product_list"),
    path("products/<int:product_id>/", views.product_detail, name="product_detail"),
    path("cart/", views.cart, name="cart"),
    path("add_to_cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path(
        "update_cart/<int:product_id>/<str:action>/",
        views.update_cart,
        name="update_cart",
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="products/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("search/", views.search_view, name="search"),
    path("category/<int:category_id>/", views.category_view, name="category"),
    path("like/", views.like_view, name="like"),
    path(
        "add_to_like/<int:product_id>/", views.add_to_like, name="add_to_like"
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
