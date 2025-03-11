from django import forms

from mailing.models import Client, Message, Mailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if hasattr(field.widget, 'attrs') and not isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-control'



class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Иван Иванов'}),
            'email': forms.EmailInput(attrs={'placeholder': 'example@email.com'}),
            'comment': forms.Textarea(attrs={'placeholder': 'Комментарий (необязательно)'})
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['name', 'message', 'client', 'frequency', 'datetime_first_mailing', 'end_datetime']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Mailing.objects.filter(name=name).exists():
            raise forms.ValidationError("Рассылка с таким названием уже существует. Придумайте другое название.")
        return name


    def clean(self):
        cleaned_data = super().clean()
        frequency = cleaned_data.get("frequency")
        end_datetime = cleaned_data.get("end_datetime")

        if frequency == "once" and end_datetime:
            self.add_error("end_datetime", "Для одноразовой рассылки не нужно указывать дату окончания.")
        if frequency != "once" and not end_datetime:
            self.add_error("end_datetime", "Для периодической рассылки необходимо указать дату окончания.")

        return cleaned_data



