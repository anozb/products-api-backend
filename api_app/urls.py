from django.urls import path
import api_app.views as api_views

urlpatterns = [
    path("", api_views.home),
    path("register/", api_views.UserRegistration.as_view(), name="user"),
    path("login/", api_views.LoginView.as_view(), name="user"),
    path("profile", api_views.UserProfile.as_view(), name="user"),
    path("products/create", api_views.ProductCreateView.as_view(), name="products"),
    path("products/list", api_views.ProductListView.as_view(), name="products"),
    path("products/detail/<int:product_id>", api_views.ProductDetailView.as_view(), name="products"),
    path("products/update/<int:product_id>", api_views.ProductUpdateView.as_view(), name="products"),
    path("products/delete/<int:product_id>", api_views.ProductDeleteView.as_view(), name="products"),

]
