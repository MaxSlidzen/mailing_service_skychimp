from django import forms
import datetime
from mailing.models import Client, Mailing


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        exclude = ('added_by',)


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        exclude = ('author', 'status',)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['client'].widget = forms.CheckboxSelectMultiple()
        self.fields['client'].queryset = Client.objects.filter(added_by=user)
        self.fields['time'].help_text = 'Введите время в формате ЧЧ:ММ'
        self.fields['start_date'].help_text = 'Введите дату в формате ДД.ММ.ГГГГ'
        self.fields['stop_date'].help_text = 'Введите дату в формате ДД.ММ.ГГГГ (необязательное поле)'

    def clean_start_date(self):
        cleaned_data = self.cleaned_data['start_date']
        if cleaned_data < datetime.date.today():
            raise forms.ValidationError('Дата старта рассылки не может быть меньше текущей')
        return cleaned_data

    def clean_stop_date(self):
        cleaned_data = self.cleaned_data['stop_date']
        if cleaned_data is not None and cleaned_data < datetime.date.today():
            raise forms.ValidationError('Дата завершения рассылки не может быть меньше текущей')
        return cleaned_data
