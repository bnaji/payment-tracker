from django.forms import ModelForm
from django import forms
from .models import Family, Lesson, CustomUser
from flatpickr import DateTimePickerInput
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class LessonUpdateForm(ModelForm):
    class Meta:
        model = Lesson
        fields = ('appt_date', 'status',)
        widgets = {'appt_date': DateTimePickerInput()}


class FamilyForm(ModelForm):
    class Meta:
        model = Family
        fields = ('client_name', 'student_name', 'address', 'price', 'starting_date', 'balance',)        
        # exclude = ('user',)
        widgets = {'starting_date': DateTimePickerInput()}

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username',)

class CustomUserChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = CustomUser
        fields = ('username',)

