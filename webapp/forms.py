from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import *
from django.forms import ModelForm


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class AssetForm(ModelForm):
    class Meta:
        model = Asset
        fields = ('name', 'journal', 'value', 'category',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = '資産名'
        self.fields['journal'].widget.attrs['class'] = 'form-control'
        self.fields['journal'].widget.attrs['placeholder'] = '帳簿'
        self.fields['value'].widget.attrs['class'] = 'form-control'
        self.fields['value'].widget.attrs['placeholder'] = '金額'
        self.fields['category'].widget.attrs['class'] = 'form-control'


class LiabilityForm(ModelForm):
    class Meta:
        model = Asset
        fields = ('name', 'journal', 'value', 'category',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = '資産名'
        self.fields['journal'].widget.attrs['class'] = 'form-control'
        self.fields['journal'].widget.attrs['placeholder'] = '帳簿'
        self.fields['value'].widget.attrs['class'] = 'form-control'
        self.fields['value'].widget.attrs['placeholder'] = '金額'
        self.fields['category'].widget.attrs['class'] = 'form-control'


class IncomeForm(ModelForm):
    class Meta:
        model = Income
        fields = ('name', 'journal', 'value', 'category',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = '収入名'
        self.fields['journal'].widget.attrs['class'] = 'form-control'
        self.fields['journal'].widget.attrs['placeholder'] = '帳簿'
        self.fields['value'].widget.attrs['class'] = 'form-control'
        self.fields['value'].widget.attrs['placeholder'] = '金額'
        self.fields['category'].widget.attrs['class'] = 'form-control'


class CostForm(ModelForm):
    class Meta:
        model = Cost
        fields = ('name', 'journal', 'value', 'category',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = '支出名'
        self.fields['journal'].widget.attrs['class'] = 'form-control'
        self.fields['journal'].widget.attrs['placeholder'] = '帳簿'
        self.fields['value'].widget.attrs['class'] = 'form-control'
        self.fields['value'].widget.attrs['placeholder'] = '金額'
        self.fields['category'].widget.attrs['class'] = 'form-control'


class JournalForm(ModelForm):
    class Meta:
        model = Journal
        fields = ('name', 'user')

    def __init__(self, *args, **kwargs):
        self.user = kwargs['user']
        super(JournalForm, self).__init__(*args, **kwargs)
        # self.fields['name'].widget.attrs['class'] = 'form-control'
        # self.fields['name'].widget.attrs['placeholder'] = '帳簿名'
        # self.fields['user'].widget.attrs['value'] = user
