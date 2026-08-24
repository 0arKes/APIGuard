from django import forms

from monitoring.models import API


class CreateAPIForm(forms.ModelForm):
    class Meta:
        model = API
        fields = ["nickname", "url", "check_interval"]

        widgets = {
            "nickname": forms.TextInput(attrs={"placeholder": "Apelido: "}),
            "url": forms.URLInput(attrs={"placeholder": "https://..."}),
            "check_interval": forms.NumberInput(attrs={"min": 1, "max": 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["check_interval"].min_value = 1
        self.fields["check_interval"].max_value = 10
        self.fields["check_interval"].initial = 5
