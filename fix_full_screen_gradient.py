#!/usr/bin/env python3
"""
Скрипт для исправления градиентов, чтобы они заливали весь экран
"""

import os
import re
from pathlib import Path

# HTML файлы для обновления
HTML_FILES = [
    'main/templates/main/home.html',
    'main/templates/main/katalog.html',
    'main/templates/main/vermietung.html',
    'main/templates/main/kontakt.html',
    'main/templates/main/neuigkeiten.html',
    'main/templates/main/datenschutz.html',
    'main/templates/main/agb.html',
    'main/templates/main/impressum.html',
    'main/templates/main/service_detail.html',
    'main/templates/main/cart.html'
]

def fix_full_screen_gradient(file_path):
    """Исправляет градиенты, чтобы они заливали весь экран"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Удаляем дублированные секции
    content = re.sub(
        r'<!-- Background Image Slider -->\s*'
        r'<div class="absolute inset-0">\s*'
        r'<div class="hero-background-slider" id="heroSlider">\s*'
        r'<!-- Динамически загружаемые картинки будут здесь -->\s*'
        r'</div>\s*'
        r'<!-- Overlay for better text readability -->\s*'
        r'<div class="absolute inset-0 bg-gradient-to-r from-blue-600/80 to-purple-600/80"></div>\s*'
        r'</div>\s*'
        r'<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">\s*'
        r'<h1[^>]*>[^<]*</h1>\s*'
        r'<p[^>]*>[^<]*</p>\s*'
        r'(?:<div[^>]*>\s*<a[^>]*>[^<]*</a>\s*</div>\s*)?'
        r'</div>\s*'
        r'</div>',
        '',
        content,
        flags=re.DOTALL
    )
    
    # Заменяем Hero секцию на полный экран
    old_hero = re.search(
        r'<!-- Hero Section with Motion Design -->\s*'
        r'<div class="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-20 relative overflow-hidden">\s*'
        r'<!-- Background Image Slider -->\s*'
        r'<div class="absolute inset-0">\s*'
        r'<div class="hero-background-slider" id="heroSlider">\s*'
        r'<!-- Динамически загружаемые картинки будут здесь -->\s*'
        r'</div>\s*'
        r'<!-- Overlay for better text readability -->\s*'
        r'<div class="absolute inset-0 bg-gradient-to-r from-blue-600/80 to-purple-600/80"></div>\s*'
        r'</div>\s*'
        r'<!-- Animated background elements -->\s*'
        r'<div class="absolute inset-0">\s*'
        r'<div class="floating-shapes">\s*'
        r'(?:<div class="shape shape-\d+"></div>\s*)*'
        r'(?:<div class="bubble bubble-\d+"></div>\s*)*'
        r'</div>\s*'
        r'</div>\s*'
        r'<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">\s*'
        r'<h1[^>]*>([^<]*)</h1>\s*'
        r'<p[^>]*>([^<]*)</p>\s*'
        r'</div>\s*'
        r'</div>',
        content,
        flags=re.DOTALL
    )
    
    if old_hero:
        title = old_hero.group(1)
        description = old_hero.group(2)
        
        new_hero = f'''<!-- Hero Section with Motion Design -->
<div class="min-h-screen bg-gradient-to-r from-blue-600 to-purple-600 text-white relative overflow-hidden">
  <!-- Background Image Slider -->
  <div class="absolute inset-0">
    <div class="hero-background-slider" id="heroSlider">
      <!-- Динамически загружаемые картинки будут здесь -->
    </div>
    <!-- Overlay for better text readability -->
    <div class="absolute inset-0 bg-gradient-to-r from-blue-600/80 to-purple-600/80"></div>
  </div>
  
  <!-- Animated background elements -->
  <div class="absolute inset-0">
    <div class="floating-shapes">
      <div class="shape shape-1"></div>
      <div class="shape shape-2"></div>
      <div class="shape shape-3"></div>
      <div class="shape shape-4"></div>
      <div class="bubble bubble-1"></div>
      <div class="bubble bubble-2"></div>
      <div class="bubble bubble-3"></div>
      <div class="bubble bubble-4"></div>
      <div class="bubble bubble-5"></div>
    </div>
  </div>
  
  <div class="flex items-center justify-center min-h-screen">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
      <h1 class="text-5xl md:text-7xl font-bold mb-6 animate-fade-in-up">{title}</h1>
      <p class="text-xl md:text-2xl mb-8 max-w-3xl mx-auto animate-fade-in-up-delay">
        {description}
      </p>
    </div>
  </div>
</div>'''
        
        content = content.replace(old_hero.group(0), new_hero)
    
    # Сохраняем обновленный файл
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Исправлен файл: {file_path}")

def main():
    """Основная функция"""
    print("🔄 Начинаю исправление градиентов для полного экрана...")
    
    for file_path in HTML_FILES:
        if os.path.exists(file_path):
            try:
                fix_full_screen_gradient(file_path)
            except Exception as e:
                print(f"❌ Ошибка при исправлении {file_path}: {e}")
        else:
            print(f"⚠️  Файл не найден: {file_path}")
    
    print("✅ Исправление завершено!")

if __name__ == "__main__":
    main() 