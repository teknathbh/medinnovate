from django import forms
from .models import *


class DoctorForm(forms.ModelForm):

    class Meta:
        model = Doctor
        fields = ('name', 'description', 'image', 'address', 'verification_document',
                  'field_of_expertise', 'tags', )
        labels = {
            'name': 'Your Name',
            'tags': 'Places willing to serve'
        }
        widgets = {
            'description': forms.Textarea(attrs={'style': 'height:65px;'}),

        }
        help_texts = {
            'tags': 'List of places nearby. Separated by comma',
        }


class InquiryForm(forms.ModelForm):

    class Meta:
        model = Inquiry
        fields = ('doctor', 'message', 'past_data', )
        widgets = {
            'doctor': forms.TextInput(attrs={'disabled': 'disabled'}),
            'past_data': forms.ClearableFileInput(attrs={'multiple': True}),
            'message': forms.Textarea(attrs={'style': 'height:30px;'}),
        }
        labels = {
            'past_data': 'Past reports or prescriptions'
        }
        help_texts = {
            'past_data': 'Can Choose Multiple',
        }


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ('name', 'long_term_illness', 'photo', 'address', )

        help_texts = {
            'long_term_illness': 'If any',
        }
