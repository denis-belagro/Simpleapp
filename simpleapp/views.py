from django.shortcuts import render
#from django.views import View # импортируем простую вьюшку
from django.core.paginator import Paginator # импортируем класс, позволяющий удобно осуществлять постраничный вывод
from .models import Product, Category
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView # импортируем класс, который говорит нам о том, что в этом представлении мы будем выводить список объектов из БД
#from datetime import datetime
from .filters import ProductFilter # импортируем недавно написанный фильтр
from .forms import ProductForm # импортируем нашу форму

class ProductsList(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 3 # поставим постраничный вывод в один элемент
    #form_class = ProductForm # добавляем форм класс, чтобы получать доступ к форме через метод POST


    """ 
    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет, полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = ProductFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        context['categories'] = Category.objects.all()
        return context
    """

    def get_filter(self):
        return ProductFilter(self.request.GET, queryset=super().get_queryset())
    def get_queryset(self):
        return self.get_filter().qs
    def get_context_data(self, *args, **kwargs):
        return {
            **super().get_context_data(*args, **kwargs),
            "filter": self.get_filter(),
            #"categories": Category.objects.all(),
            #"form": ProductForm(), 
        }

"""
    def post(self, request, *args, **kwargs):
        # берём значения для нового товара из POST-запроса отправленного на сервер
        
        name = request.POST['name']
        quantity = request.POST['quantity']
        category_id = request.POST['category']
        price = request.POST['price']
 
        product = Product(name=name, quantity=quantity, category_id=category_id, price=price) # создаём новый товар и сохраняем
        product.save()
        
        form = self.form_class(request.POST) # создаём новую форму, забиваем в неё данные из POST-запроса 
 
        if form.is_valid(): # если пользователь ввёл всё правильно и нигде не накосячил, то сохраняем новый товар
            form.save()

        return super().get(request, *args, **kwargs) # отправляем пользователя обратно на GET-запрос.    
        """

# В отличие от дженериков, которые мы уже знаем, код здесь надо писать самому, переопределяя типы запросов (например, get- или post-)
"""
class ProductsList(View):
    
    def get(self, request):
        products = Product.objects.order_by('-price')
        p = Paginator(products, 1) # создаём объект класса пагинатор, передаём ему список наших товаров и их количество для одной страницы
 
        products = p.get_page(request.GET.get('page', 1)) # берём номер страницы из get-запроса. Если ничего не передали, будем показывать первую страницу.
        # теперь вместо всех объектов в списке товаров хранится только нужная нам страница с товарами
        
        data = {
            'products': products,
        }
        return render(request, 'products.html', data)
        """

""" 
class ProductsList(ListView):
    model = Product  # указываем модель, объекты которой мы будем выводить
    template_name = 'products.html'  # указываем имя шаблона, в котором будет лежать HTML, в нём будут все инструкции о том, как именно пользователю должны вывестись наши объекты
    context_object_name = 'products'  # это имя списка, в котором будут лежать все объекты, его надо указать, чтобы обратиться к самому списку объектов через HTML-шаблон
    queryset = Product.objects.order_by('-id')

     # метод get_context_data нужен нам для того, чтобы мы могли передать переменные в шаблон. В возвращаемом словаре context будут храниться все переменные. Ключи этого словари и есть переменные, к которым мы сможем потом обратиться через шаблон
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow() # добавим переменную текущей даты time_now
        context['value1'] = None # добавим ещё одну пустую переменную, чтобы на её примере посмотреть работу другого фильтра
        return context
"""
# создаём представление, в котором будут детали конкретного отдельного товара
"""
class ProductDetail(DetailView):
    model = Product # модель всё та же, но мы хотим получать детали конкретно отдельного товара
    template_name = 'product.html' # название шаблона будет product.html
    context_object_name = 'product' # название объекта 
"""

# дженерик для получения деталей о товаре
class ProductDetailView(DetailView):
    template_name = 'product_detail.html'
    queryset = Product.objects.all()
 
 
# дженерик для создания объекта. Надо указать только имя шаблона и класс формы который мы написали в прошлом юните. Остальное он сделает за вас
class ProductCreateView(CreateView):
    template_name = 'product_create.html'
    form_class = ProductForm

# дженерик для редактирования объекта
class ProductUpdateView(UpdateView):
    template_name = 'product_create.html'
    form_class = ProductForm
 
    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Product.objects.get(pk=id)
 
 
# дженерик для удаления товара
class ProductDeleteView(DeleteView):
    template_name = 'product_delete.html'
    queryset = Product.objects.all()
    success_url = '/products/'
