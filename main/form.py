from django.forms import ModelForm
from .models import *

class chequeInfoForm(ModelForm):
    class Meta:
        model = chequeInfo
        fields = "__all__"