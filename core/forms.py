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
        fields = ('message', 'past_data', 'reference_file_1',
                  'reference_file_2', 'reference_file_3', )
        widgets = {
            'message': forms.Textarea(attrs={'style': 'height:30px;'}),
        }
        labels = {
            'past_data': 'Related reports or prescriptions'
        }


class PersonForm(forms.ModelForm):

    class Meta:
        model = Person
        fields = ('name', 'long_term_illness', 'photo', 'address', )

        help_texts = {
            'long_term_illness': 'If any',
        }
