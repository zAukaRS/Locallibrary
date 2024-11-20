from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from .views import BorrowBookView, BookCreateView, BookUpdateView, BookDeleteView, add_beloved_book

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('my_borrowed/', views.MyBorrowedView.as_view(), name='my_borrowed'),
    path('all_borrowed_books/', views.BorrowedBooksByLibrarianView.as_view(), name='all_borrowed_books'),
    path('book/<uuid:pk>/borrow/', BorrowBookView.as_view(), name='borrow_book'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew_book_librarian'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    path('books/create/', BookCreateView.as_view(), name='book_create'),
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book_update'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
    path('book/<int:pk>/add_beloved/', add_beloved_book, name='add_beloved_book'),
]
