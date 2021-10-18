from django.forms import ModelForm, BooleanField # Импортируем true-false поле
from .models import Product
 
 
# Создаём модельную форму
class ProductForm(ModelForm):
    check_box = BooleanField(label='Привет') # добавляем галочку или же true-false поле
 
    # в класс мета, как обычно, надо написать модель, по которой будет строиться форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'quantity', 'check_box'] # не забываем включить галочку в поля, иначе она не будет показываться на странице!
