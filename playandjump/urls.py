from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # главная и статические страницы
    path('katalog/', include('catalog.urls')),  # ← здесь подключаем каталог
    path('warenkorb/', include('cart.urls')),
]

# Добавляем URL для медиафайлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
