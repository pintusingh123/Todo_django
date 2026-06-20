from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import re
from django.core.exceptions import ValidationError


class Registration(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        style = "w-full px-4 py-3 border text-white border-slate-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"

        self.fields["username"].widget.attrs.update({
            "class": style,
            "placeholder": "Enter Your username"
        })

        self.fields["email"].widget.attrs.update({
            "class": style,
            "placeholder": "Enter Your Email"
        })

        self.fields["password1"].widget.attrs.update({
            "class": style,
            "placeholder": "Enter New password"
        })

        self.fields["password2"].widget.attrs.update({
            "class": style,
            "placeholder": "Confirm password"
        })

    # 🔥 EMAIL UNIQUE CHECK
    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already used. Try another email.")

        return email

    #  USERNAME VALIDATION (NEW ADDED)
    def clean_username(self):
        username = self.cleaned_data.get("username")

        # length check
        if len(username) < 3 or len(username) > 15:
            raise ValidationError("Username must be 3–15 characters long.")

        # only letters, numbers, underscore allowed
        if not re.match(r"^[a-zA-Z0-9_]+$", username):
            raise ValidationError(
                "Username can only contain letters, numbers, underscore.")

        # duplicate check
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already taken.")

        return username


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        style = """
        w-full px-4 py-3 
        text-white 
        border border-slate-600 
        rounded-xl 
        focus:outline-none focus:ring-2 focus:ring-indigo-900 focus:border-indigo-500
        placeholder:text-slate-400
        """

        self.fields["username"].widget.attrs.update({
            "class": style.strip(),
            "placeholder": "Enter Yur username",
            "autocomplete": "off"
        })

        self.fields["password"].widget.attrs.update({
            "class": style.strip(),
            "placeholder": "Enter Your password",
            "autocomplete": "off"
        })
