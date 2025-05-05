from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import UsersAccounts


class UsersAccountsAdminForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = UsersAccounts
        fields = '__all__'

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password:
            validate_password(password)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        raw_password = self.cleaned_data["password"]
        user.set_password(raw_password)
        if commit:
            user.save()
        return user