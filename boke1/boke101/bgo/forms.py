
from django import forms

class ArticleForm(forms.Form):

    title = forms.CharField(required=True, error_messages={'required':'文章标题必填'})
    content = forms.CharField(required=True, error_messages={'required':'文章内容必填'})
    tags = forms.CharField(required=True, error_messages={'required':'文章标签必填'})
    describe = forms.CharField(required=True, error_messages={'required':'文章描述必填'})
    upload_img = forms.ImageField(required=False)


