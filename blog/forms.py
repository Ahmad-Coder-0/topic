from email.policy import default
from django import forms
from .models import *


class TicketForm(forms.Form):
    SUBJECT_CHOICES = (
        ('پیشنهاد', 'پیشنهاد'),
        ('انتقاد', 'انتقاد'),
        ('گزارش', 'گزارش مشکل')
    )
    name = forms.CharField(max_length=100, required=True, label='نام')
    message = forms.CharField(widget=forms.Textarea,
                              required=True, label='متن')
    email = forms.EmailField(label='ایمیل', required=False)
    phone = forms.CharField(max_length=11, required=True, label='شماره موبایل')
    subject = forms.ChoiceField(choices=SUBJECT_CHOICES, label='موضوع')

    def clean_name(self):
        entry_name = self.cleaned_data['name']
        if entry_name:
            if not entry_name.replace(' ', '').isalpha() or len(entry_name) < 3:
                raise forms.ValidationError('نام خود را صحیح وارد کنید')
            else:
                c = 0
                name = ''
                space = False
                for i in entry_name:
                    if i.isalpha():
                        name += i
                        c += 1
                        if c >= 3:
                            space = True
                    if i.isspace() and space:
                        name += i
                        space = False
                        c = 0
                return name

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if phone:
            if not phone.isnumeric() or len(phone) != 11:
                raise forms.ValidationError('شماره موبایل صحیح نیس!')
            else:
                return phone

    def clean_message(self):
        message = self.cleaned_data['message']
        if message:
            if len(message.replace(' ', '')) < 10:
                raise forms.ValidationError('پیام شما کوتاه است')
            else:
                return message


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'message']


class PostForm(forms.ModelForm):
    image1 = forms.ImageField(label="تصویر اول", required=False)
    image2 = forms.ImageField(label="تصویر دوم", required=False)
    class Meta:
        model = Post
        fields = ['title', 'description', 'reading_time']
        
class SearchForm(forms.Form):
    query = forms.CharField()
