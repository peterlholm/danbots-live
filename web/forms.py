from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from common.models import  Scanner #Clinic,

class ScannerForm(forms.ModelForm):
    class Meta:
        model = Scanner
        fields = ['Serial', 'Clinic','Charge','LastRegister']

    def __init__(self, *args, **kwargs):
        super(ScannerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-4'   # control-label
        self.helper.field_class = 'col-sm-6'
        self.helper.form_tag = True
        self.helper.add_input(Submit('submit', 'Send'))
        self.helper.add_input(Submit('cancel', 'Fortryd', css_class='btn-secondary', formnovalidate='formnovalidate', formaction='/'))
