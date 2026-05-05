from django import forms
from django.db.models import BooleanField

from .models import Product

FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]

class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = "form-check-input"
            else:
                fild.widget.attrs['class'] = "form-control"


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('views_counter', 'owner')

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        self.fields['product_name'].widget.attrs.update({
            'class': 'form-control',  # Добавление CSS-класса для стилизации поля
            'placeholder': 'Введите название продукта'  # Текст подсказки внутри поля
        })

        self.fields['description'].widget.attrs.update({
            'class': 'form-control',  # Добавление CSS-класса для стилизации поля
            'placeholder': 'Введите описание продукта'  # Текст подсказки внутри поля
        })

        # Настройка атрибутов виджета для поля 'email'
        self.fields['category_name'].widget.attrs.update({
            'class': 'form-control',  # Добавление CSS-класса для стилизации поля
            'placeholder': 'Выберите категорию продукта'  # Текст подсказки внутри поля
        })

        self.fields['product_cost'].widget.attrs.update({
            'class': 'form-control',  # Добавление CSS-класса для стилизации поля
            'placeholder': 'Введите стоимость продукта'  # Текст подсказки внутри поля
        })

    def clean(self):
        cleaned_data = super().clean()
        product_name = cleaned_data.get('product_name')
        description = cleaned_data.get('description')

        for word in FORBIDDEN_WORDS:
            # Проверка в названии продукта
            if word in product_name.lower():
                self.add_error('product_name', f'Запрещено использовать слово: "{word}"')

            # Проверка в описании продукта
            if word in description.lower():
                self.add_error('description', f'Запрещено использовать слово: "{word}"')

        return cleaned_data

    def clean_product_cost(self):
        product_cost = self.cleaned_data.get('product_cost')

        if product_cost < 0:
            raise forms.ValidationError(
                'Цена не может быть отрицательной.'
            )

        return product_cost

class ProductModeratorForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        # fields = ('views_counter', 'owner')


