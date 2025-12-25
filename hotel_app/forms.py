from django import forms
from .models import RoomType, Room, Price, Booking
from datetime import date

class RoomTypeForm(forms.ModelForm):
    class Meta:
        model = RoomType
        fields = ['name', 'description']
        labels = {
            'name': 'Название типа номера',
            'description': 'Описание',
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number', 'room_type', 'category', 'capacity', 'has_baby_bed', 'is_available', 'price_per_night']
        labels = {
            'room_number': 'Номер комнаты',
            'room_type': 'Тип номера',
            'category': 'Категория',
            'capacity': 'Вместимость',
            'has_baby_bed': 'Детская кроватка',
            'is_available': 'Доступен',
            'price_per_night': 'Цена за ночь',
        }
        widgets = {
            'has_baby_bed': forms.CheckboxInput(),
            'is_available': forms.CheckboxInput(),
        }

class PriceForm(forms.ModelForm):
    class Meta:
        model = Price
        fields = ['room_type', 'day_of_week', 'price']
        labels = {
            'room_type': 'Тип номера',
            'day_of_week': 'День недели',
            'price': 'Цена',
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['customer_name', 'customer_phone', 'room', 'check_in_date', 'check_out_date']
        labels = {
            'customer_name': 'Имя клиента',
            'customer_phone': 'Телефон клиента',
            'room': 'Номер',
            'check_in_date': 'Дата заезда',
            'check_out_date': 'Дата выезда',
        }
        widgets = {
            'customer_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'tel',
                'inputmode': 'tel',
                'autocomplete': 'tel',
                'pattern': '[0-9+\-\s\(\)]*',
                'placeholder': '+7 (XXX) XXX-XXXX'
            }),
            'check_in_date': forms.DateInput(attrs={'type': 'date'}),
            'check_out_date': forms.DateInput(attrs={'type': 'date'}),
        }

class CheckInForm(forms.Form):
    """Форма для регистрации заезда гостя"""
    customer_name = forms.CharField(
        label='Имя клиента',
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    customer_phone = forms.CharField(
        label='Телефон клиента',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'tel',
            'inputmode': 'tel',
            'autocomplete': 'tel',
            'pattern': '[0-9+\-\s\(\)]*',
            'placeholder': '+7 (XXX) XXX-XXXX'
        })
    )
    customer_email = forms.EmailField(
        label='Электронная почта',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    room_type = forms.ModelChoiceField(
        label='Тип номера',
        queryset=RoomType.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    has_baby_bed = forms.BooleanField(
        label='Детская кроватка',
        required=False,
        widget=forms.CheckboxInput()
    )
    check_in_date = forms.DateField(
        label='Дата заезда',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'lang': 'ru'}),
        initial=lambda: date.today()
    )
    check_out_date = forms.DateField(
        label='Дата выезда',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'lang': 'ru'}),
        initial=lambda: date.today()
    )
