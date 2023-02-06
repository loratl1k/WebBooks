from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from .models import Book, Author, BookInstance, Genre, Compare
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(
        status__exact=2).count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    return render(request, 'index.html', context={
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits
    })


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        in_compare = Compare.objects.filter(
            user=self.request.user,
            book=self.kwargs['pk'],
        ).exists()
        context['in_compare'] = in_compare
        return context


class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/book_instance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects \
            .filter(borrower=self.request.user) \
            .filter(status__exact='1') \
            .order_by('due_back')


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
