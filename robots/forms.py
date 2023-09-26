from django.forms import (
    Form,
    TextInput,
    DateTimeInput, DateTimeField, CharField,

)
from .models import Robot

class RobotForm(Form):
    model = CharField(max_length=2)
    version = CharField(max_length=2)
    created = DateTimeField(
        input_formats=['%Y-%m-%d %H:%M:%S'],  # формат ввода даты и времени
        widget=DateTimeInput(attrs={ 'placeholder': 'YYYY-MM-DD HH:MM:SS'})
    )
