from django import forms
from .models import *


class LteForm(forms.ModelForm):
    class Meta:
        model = lte_integration
        fields= ('id','site', 'service', 'type', 'task', 'date', 'executor', 'domain','ticket','remarks')


class ComputerSearchForm(forms.ModelForm):
    class Meta:
        model = lte_integration
        fields = ['site', 'service', 'type', 'task', 'date', 'executor']

class ValidSearchForm(forms.ModelForm):
    class Meta:
        model = lte_validation
        fields = ['executor', 'date', 'domain']