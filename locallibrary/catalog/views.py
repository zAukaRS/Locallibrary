from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic import ListView, FormView, CreateView, UpdateView, DeleteView
import datetime
from django.db.models import Q
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .forms import RenewBookForm, BorrowBookForm, BookForm
from .models import Book, Author, BookInstance


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


class MyBorrowedView(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'my_borrowed.html'
    context_object_name = 'borrowed_books'

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user, status='o')


class BorrowedBooksByLibrarianView(PermissionRequiredMixin, ListView):
    model = BookInstance
    template_name = 'all_borrowed_books.html'
    context_object_name = 'borrowed_books'
    permission_required = 'catalog.can_mark_returned'

    def get_queryset(self):
        return BookInstance.objects.filter(status='o').order_by('due_back')


class BorrowBookView(LoginRequiredMixin, FormView):
    template_name = 'borrow_book.html'
    form_class = BorrowBookForm

    def form_valid(self, form):
        book_instance_id = self.kwargs['pk']
        book_instance = get_object_or_404(BookInstance, pk=book_instance_id)

        if book_instance.status != 'a':
            form.add_error(None, "Эта книга уже занята.")
            return self.form_invalid(form)

        book_instance.borrower = self.request.user
        book_instance.due_back = form.cleaned_data['due_back']
        book_instance.status = 'o'  # Меняем статус на "взята"
        book_instance.save()

        return redirect('index')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    if request.method == 'POST':
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_instance.due_back = form.cleaned_data['due_back']
            book_instance.save()

            return HttpResponseRedirect(reverse('all_borrowed_books'))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'book_renew_librarian.html', context)


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': ''}
    permission_required = 'catalog.add_author'
    template_name = 'author_form.html'


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    template_name = 'author_update.html'
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.change_author'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Обновить сведения об авторе"
        return context


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    template_name = 'author_delete.html'
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.delete_author'

    def form_valid(self, form):
        try:
            self.object.delete()
            return HttpResponseRedirect(self.success_url)
        except Exception:
            return HttpResponseRedirect(
                reverse("author-delete", kwargs={"pk": self.object.pk})
            )


@method_decorator(permission_required('catalog.add_book'), name='dispatch')
class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'book_form.html'
    success_url = reverse_lazy('book_list')


@method_decorator(permission_required('catalog.change_book'), name='dispatch')
class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'book_form.html'
    success_url = reverse_lazy('book_list')


@method_decorator(permission_required('catalog.delete_book'), name='dispatch')
class BookDeleteView(DeleteView):
    model = Book
    template_name = 'book_confirm_delete.html'
    success_url = reverse_lazy('book_list')

    def form_valid(self, form):
        if self.object.bookinstance_set.exists():
            return redirect('book_list')
        return super().form_valid(form)
