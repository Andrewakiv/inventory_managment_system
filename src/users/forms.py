from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile


class RegistrationForm(UserCreationForm):
    company_name = forms.CharField(max_length=255)

    class Meta:
        model = CustomUser
        fields = ("name", "surname", "email", "company_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True
        user.save()
        company_name = self.cleaned_data["company_name"]
        Profile.objects.create(person=user, name=company_name)
        return user


class ProfileForm(forms.ModelForm):
    company_name = forms.CharField(max_length=255)

    class Meta:
        model = CustomUser
        fields = ["name", "surname", "email", "company_name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].disabled = True

        if self.instance and self.instance.profile:
            self.fields["company_name"].initial = self.instance.profile.name

    def save(self, commit=True):
        user = super().save(commit=False)
        company_name = self.cleaned_data.get("company_name")

        if user.profile:
            user.profile.name = company_name
            user.profile.save()

        if commit:
            user.save()

        return user
