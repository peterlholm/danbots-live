from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from common.models import Clinic, Scanner

class UserForm(forms.Form):
    Login = forms.CharField(required=True, label='Login', max_length=50, strip=True)
    FirstName = forms.CharField(required=True, label='Fornavn', max_length=50, strip=True)
    LastName = forms.CharField(required=True, label='Efternavn', max_length=50, strip=True)
    Password = forms.CharField(required=True, label='Password', max_length=50, strip=True)
    Email = forms.EmailField(required=True, label='Email', max_length=90)
    ClinicNo = forms.IntegerField(required=True, label='Kliniknummer', min_value=0)
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'   # control-label
        self.helper.field_class = 'col-sm-6'
        self.helper.form_tag = True
        self.helper.add_input(Submit('submit', 'Send'))
        self.helper.add_input(Submit('cancel', 'Fortryd', css_class='btn-secondary', formnovalidate='formnovalidate', formaction='/'))

class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = ['No', 'Name','Logo']

    def __init__(self, *args, **kwargs):
        super(ClinicForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'   # control-label
        self.helper.field_class = 'col-sm-6'
        self.helper.form_tag = True
        self.helper.add_input(Submit('submit', 'Send'))
        self.helper.add_input(Submit('cancel', 'Fortryd', css_class='btn-secondary', formnovalidate='formnovalidate', formaction='/'))

class ScannerForm(forms.ModelForm):
    class Meta:
        model = Scanner
        fields = ['Serial', 'Clinic','Charge','LastRegister']

