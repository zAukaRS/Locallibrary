from django.contrib import admin
from .models import Book, Author, Genre, Language, BookInstance

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth', 'date_of_death')
    search_fields = ('first_name', 'last_name')
    list_display_links = ('name',)

    def name(self, obj):
        return f'{obj.first_name} {obj.last_name}'
    name.short_description = 'Полное имя'

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'language', 'isbn')
    list_filter = ('author', 'genre', 'language')
    search_fields = ('title', 'author__first_name', 'author__last_name')
    list_display_links = ('title',)
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
    list_display = ('book', 'status', 'due_back', 'borrower')
    list_filter = ('status', 'due_back')
    search_fields = ('book__title', 'borrower__username')
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
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
