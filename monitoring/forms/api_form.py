from django import forms

from monitoring.models import API


class APIForm(forms.ModelForm):
    class Meta:
        model = API
        fields = ["nickname", "url"]

        widgets = {
            "nickname": forms.TextInput(attrs={"placeholder": "Apelido: "}),
            "url": forms.URLInput(attrs={"placeholder": "https://..."}),
        }
