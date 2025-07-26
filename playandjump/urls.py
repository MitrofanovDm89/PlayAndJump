from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # главная и статические страницы
    path('katalog/', include('catalog.urls')),  # ← здесь подключаем каталог
    path('warenkorb/', include('cart.urls')),

]
