from django.urls import path
from .views import *

urlpatterns = [
   path("authors", authors_list, name="authors"),
   path("authors/<int:pk>", author_details, name="author_details"),
   path("authors/books/<int:pk>", book_by_author, name="book_by_author"),

   path("books", books_list, name="books"),
   path("books/<int:pk>", book_details, name="book_details"),
   path("books/category/<int:pk>", category_books, name="category_books"),

   path("categories", categories_list, name="categories"),
   path("categories/<int:pk>", category_details, name="category_details"),

   path("search/<str:query>", search_book_author, name="search"),

   path("comments/<int:book_id>", book_comments, name="comments"),
   path("comment/<int:book_id>", add_comment, name="add_comment"),
   path("comment/opt/<int:pk>", comment_option, name="comment_option"),
]
