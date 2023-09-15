from django import forms

from blog.models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        exclude = ('views_count',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
