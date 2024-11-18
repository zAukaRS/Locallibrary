from django.shortcuts import render
from django.views import generic, View
from .models import Book, Author
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def index(request):
    search_word = request.GET.get('q', '')

    num_books = Book.objects.all().count()
    num_authors = Author.objects.all().count()

    if search_word:
        num_books_with_word = Book.objects.filter(
            Q(title__icontains=search_word) | Q(description__icontains=search_word)
        ).count()
        genres_with_books = Book.objects.filter(
            Q(title__icontains=search_word) | Q(description__icontains=search_word)
        ).values_list('genre', flat=True).distinct()
        num_genres_with_books = genres_with_books.count()
    else:
        num_books_with_word = 0
        num_genres_with_books = 0

    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] = num_visits

    context = {
        'num_books': num_books,
        'num_authors': num_authors,
        'num_books_with_word': num_books_with_word,
        'num_genres_with_books': num_genres_with_books,
        'search_word': search_word,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    context_object_name = 'book_list'
    template_name = 'book_list.html'
    paginate_by = 5

    def get_queryset(self):
        return Book.objects.all()


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'book_detail.html'


class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    context_object_name = 'authors'
    template_name = 'authors.html'

    def get_queryset(self):
        return Author.objects.all()


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author
    context_object_name = 'author'
    template_name = 'author_detail.html'


class MyBorrowedView(View):
    def get(self, request):
        return render(request, 'my_borrowed.html')


