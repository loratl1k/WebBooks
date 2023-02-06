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
