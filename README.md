### Реализуйте возможность сравнения книг. На странице с информацией о книге добавить ссылку «Добавить к сравнению». Реализовать страницу, на которой бы отображались характеристики всех добавленных к сравнению пользователем книг.

В файле models.py была создан класс ``` Compare ```. Для хранения информации о 
книге создано поле book, которое по первичному ключу связано с моделью 
```Book```. Для хранения информации о пользователе создано поле user, которое по 
первичному ключу связано с моделью ```User```. :

```
class Compare(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE,
                             related_name='comparing_books')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
```

Далее для отображения кнопки для добавления книги к сравнению в файле 
book_detail.html был добавлен следующий код после {% endfor %}:

```
  <div>
    {% if in_compare %}

    {% else %}
    <a class="btn btn-primary" href="{% url 'catalog:to_compare' book.id %}"
       role="button" />Добавить к сравнению
    </a>
    {% endif %}
  </div>
```
в base.html был изменён код следующим образом, для повяления в верхней панели
сайта кнопки "Мои сравнения", при нажатии на которую будут сопоставлены книги, 
добавленные к сравнению:
```
 <nav class="nav">
                <a href="{%url 'catalog:books'%}" class="nav-link">Книги</a>
                <a href="{%url 'catalog:authors'%}" class="nav-link">Авторы</a>
                {%if user.is_authenticated%}
                <a href="{%url 'catalog:my-borrowed'%}" class="nav-link">Мои
                    заказы</a>
                <a href="{%url 'catalog:compare'%}" class="nav-link">Мои
                    сравнения</a>
                {%endif%}
                
            </nav>
```

После чего я добавил новые ссылки в urls.py, на которые перекидывает пользователя 
сайта при нажатии на копку "Добавить к сравнению" и при нажатии на "Мои сравнения" 
в верхней панели сайта, и файл начал выглядеть следующим образом:

```
from django.urls import path, re_path
from . import views


app_name = "catalog"
urlpatterns = [
    path("", views.index, name="index"),
    re_path(r"^books/$", views.BookListView.as_view(), name="books"),
    re_path(r"^book/(?P<pk>\d+)$",
            views.BookDetailView.as_view(), name="book-detail"),
    re_path(r"^authors/$", views.AuthorListView.as_view(),
            name="authors"),
    re_path(r"^mybooks/$", views.LoanedBooksByUserListView.as_view(),
            name="my-borrowed"),
    path("to_compare/<int:book_id>", views.to_compare, name="to_compare"),
    path("compare", views.compare, name="compare"),
]
```
Дальше в viewes.py были добавлены функции ```to_compare``` и ```compare``` 
для обработки того, что происходит при нажатии на копку "Добавить к сравнению" 
и при нажатии на "Мои сравнения" в верхней панели сайта. :

```
def to_compare(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    Compare.objects.create(
        user=request.user,
        book=book,
    )
    return redirect('catalog:book-detail', pk=book_id)


def compare(request):
    books = Compare.objects.filter(
        user=request.user
    )
    context = {
        'title': 'Сравнение книг',
        'books': books,
    }
    template = 'catalog/book_compare.html'
    return render(request, template, context)
```
И напоследок был создан book_compare.html, показывающий как будет выглядеть
сайт "Мир книг" при нажатии на "Мои сравнения" в верхней панели сайта.

```
{%extends 'base.html'%}


{% block content %}
<h1>{{title}}</h1>
<table class="table">
  <thead>
    <tr>
      <th scope="col">Название книги</th>
      <th scope="col">Жанр книги</th>
      <th scope="col">Язык книги</th>
      <th scope="col">Автор книги</th>
      <th scope="col">Аннотация книги</th>
      <th scope="col">ISBN</th>
    </tr>
  </thead>
  <tbody>
  {% for book in books.all %}
    <tr>
      <td>{{ book.book.title }}</td>
      <td>{{ book.book.genre }}</td>
      <td>{{ book.book.language }}</td>
      <td>
      {% for author in book.book.author.all %}
        <div>{{ author }}</div>
      {% endfor %}
      </td>
      <td>{{ book.book.summary }}</td>
      <td>{{ book.book.isbn }}</td>
    </tr>
  {% endfor %}
  </tbody>
</table>


{% endblock  %}
```