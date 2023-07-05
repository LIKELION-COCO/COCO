from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('', lambda request: redirect('user:signin')),
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('town/', include('town.urls')),
    path('myPage/', include('myPage.urls')),
    path('blog/', include('blog.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)