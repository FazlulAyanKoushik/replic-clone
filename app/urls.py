from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar

schema_view = get_schema_view(
    openapi.Info(
        title="Repliq e-Commerce",
        default_version="v1",
        description="This is a demo e-commerce website using django rest-framework.",
        terms_of_service="https://www.ourapp.com/policies/terms/",
        contact=openapi.Contact(email="kf.ayan17@gmail.com"),
        license=openapi.License(name="License @Fazlul Ayan Koushik"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Swagger
    path(
        "api/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    # Debug Toolbar
    path("__debug__/", include("debug_toolbar.urls")),
    # App urls
    path("admin/", admin.site.urls),
    path("api/users", include("accounts.urls")),
    path("api/categories/", include("category.urls")),
    path("api/reviews/", include("review.urls")),
    path("api/products/", include("product.urls")),
    path("api/carts/", include("cart.urls")),
    path("api/orders/", include("order.urls")),
    path("api/shipping/address/", include("shipping_address.urls")),
    # Admin app Urls
    path("api/admin/categories/", include("core.category_urls")),
    path("api/admin/discounts/", include("core.discount_urls")),
    path("api/admin/tags", include("core.tag_urls")),
    path("api/admin/products", include("core.product_urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
