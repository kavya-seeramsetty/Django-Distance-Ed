from django import forms
from django.forms import SelectDateWidget

from myappF23.models import Order, Student, Instructor


class InterestForm(forms.Form):
    INTEREST_CHOICES = (
        (1, 'Yes'),
        (0, 'No'),
    )

    interested = forms.IntegerField(
        label='Interested',
        widget=forms.RadioSelect(choices=INTEREST_CHOICES),
        # choices=INTEREST_CHOICES,
        initial=1,
        required=True
    )

    levels = forms.IntegerField(
        label='Levels',
        initial=1,
        min_value=1,
        required=True
    )

    comments = forms.CharField(
        label='Additional Comments',
        widget=forms.Textarea,
        required=False
    )


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['student', 'course', 'levels', 'order_date']

    # Customize the widget for the 'student' field
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        widget=forms.RadioSelect
    )

    # Customize the widget for the 'order_date' field
    order_date = forms.DateField(widget=SelectDateWidget())



