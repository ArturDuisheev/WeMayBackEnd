from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="WeMay API",
        default_version='v1',
        description="API for WeMay project",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="myworkingartir@gmail.com",),
        license=openapi.License(name="License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny,]
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # пути для приложений
    path('api/v1/users/', include('user.urls')),
    path('api/v1/promotions/', include('promotion.urls')),
    path('api/v1/reviews/', include('review.urls')),
    path('api/v1/company/', include('company.urls')),

    # Auth URL с использованием djoser
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/token/', include('djoser.urls.authtoken')),
    path('api/v1/auth/jwt/', include('djoser.urls.jwt')),

    # OAuth2 URL
    path('api/v1/oauth/', include('drf_social_oauth2.urls', namespace='drf')),

    # Swagger и Redoc
    path('swagger<str:format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
