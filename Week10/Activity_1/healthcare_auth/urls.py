from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    # Redirect root to login page
    path('', RedirectView.as_view(url='/api/auth/login-page/', permanent=False)),
]
