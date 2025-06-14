from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Обязательно. Пример: user@example.com')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class RateMovieForm(forms.Form):
    rating = forms.IntegerField(
        min_value=1, 
        max_value=10, 
        widget=forms.NumberInput(attrs={'type':'number', 'placeholder': '1-10'}),
        label="Ваша оценка"
    )