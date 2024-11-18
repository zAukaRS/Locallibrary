from django.contrib import admin
from .models import Book, Author, Genre, Language, BookInstance

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth', 'date_of_death')  # Используем свойство name
    search_fields = ('first_name', 'last_name')  # Поиск по имени и фамилии
    list_display_links = ('name',)  # Ссылки для редактирования

    def name(self, obj):
        return f'{obj.first_name} {obj.last_name}'
    name.short_description = 'Полное имя'

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'language', 'isbn')  # Название, автор, язык, ISBN
    list_filter = ('author', 'genre', 'language')  # Фильтры
    search_fields = ('title', 'author__first_name', 'author__last_name')  # Поиск по названию и автору
    list_display_links = ('title',)  # Ссылки для редактирования
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'author', 'description', 'genre', 'language')
        }),
        ('Дополнительная информация', {
            'fields': ('isbn',)
        }),
    )

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back', 'borrower')  # Книга, статус, возврат, заемщик
    list_filter = ('status', 'due_back')  # Фильтры
    search_fields = ('book__title', 'borrower__username')  # Поиск по книге и заемщику
    fieldsets = (
        ('Информация о книге', {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Доступность', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Название жанра
    search_fields = ('name',)  # Поиск по названию

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Язык
    search_fields = ('name',)  # Поиск по языку
