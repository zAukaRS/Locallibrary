from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import BookInstance, Book
import datetime


class RenewBookForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ['due_back']
        labels = {'due_back': _('Дата возврата')}
        help_texts = {'due_back': _('Введите дату в пределах 4 недель от сегодня.')}
        widgets = {
            'due_back': forms.SelectDateWidget(),
        }

    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        if data < datetime.date.today():
            raise ValidationError(_('Неверная дата — она уже прошла.'))

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Неверная дата — больше чем на 4 недели вперед.'))

        return data


class BorrowBookForm(forms.Form):
    due_back = forms.DateField(
        label="Дата возврата",
        widget=forms.SelectDateWidget(),
        initial=datetime.date.today() + datetime.timedelta(weeks=2),
    )

    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        if data < datetime.date.today():
            raise forms.ValidationError('Дата возврата не может быть в прошлом.')

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise forms.ValidationError('Дата возврата не может быть позже, чем через 4 недели.')

        return data


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'isbn', 'genre']
        labels = {
            'title': 'Название',
            'author': 'Автор',
            'description': 'Описание',
            'isbn': 'ISBN',
            'genre': 'Жанры',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'genre': forms.CheckboxSelectMultiple(),
        }

        def clean_genre(self):
            genres = self.cleaned_data.get('genre')
            if genres and genres.count() > 3:
                raise forms.ValidationError("Вы не можете выбрать больше 3 жанров.")
            return genres
