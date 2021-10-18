from django.urls import path
from .views import ProductsList, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView # импортируем наше представление
 
 
urlpatterns = [
    # path — означает путь. В данном случае путь ко всем товарам у нас останется пустым, позже станет ясно почему
    path('', ProductsList.as_view()), # т.к. сам по себе это класс, то нам надо представить этот класс в виде view. Для этого вызываем метод as_view
    #path('<int:pk>', ProductDetail.as_view()),  # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
     path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'), # Ссылка на детали товара
    path('create/', ProductCreateView.as_view(), name='product_create'), # Ссылка на создание товара

]