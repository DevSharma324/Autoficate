from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django import forms

from .models import CustomUser, DataItemSetModel, ImageModel

from fontTools.ttLib import TTFont
import os


# Form for New User Signup
class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "user_email", "password1", "password2", "allow_promotional"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_user_email(self):
        user_email = self.cleaned_data.get("user_email")

        if CustomUser.objects.filter(
            user_email=user_email
        ).exists() and CustomUser.objects.get(user_email=user_email).check_password(""):
            raise ValidationError("A user with this email already exists.")

        else:
            pass

        return user_email

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# Form for first Time User Login
class NameSignUpForm(forms.Form):
    first_name = forms.CharField(
        max_length=30,
        label="User First Name",
    )
    last_name = forms.CharField(
        max_length=30,
        label="User Last Name",
    )
    user_email = forms.EmailField(
        max_length=255,
        label="User Email",
        required=False,
    )


# Form for User Login
class LoginForm(forms.Form):
    user_email = forms.EmailField(label="Email", required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


# Form for Excel file Input
class ExcelForm(forms.Form):
    excel_file = (
        forms.FileField()
    )  # (widget=forms.TextInput(attrs={'id': 'file-upload'}))


# Form for Image file Input
class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageModel
        fields = ["image"]


def get_available_fonts():
    font_dir = os.path.join("static", "fonts")
    font_files = [f for f in os.listdir(font_dir) if f.endswith(".ttf")]

    font_list = []
    for font_file in font_files:
        font_path = os.path.join(font_dir, font_file)
        try:
            font = TTFont(font_path)
            font_name = font["name"].getName(1, 3, 1).toUnicode()
            font_list.append((font_name, font_name))
        except Exception as e:
            print(f"Error processing font file {font_file}: {e}")

    return font_list


class ItemForm(forms.ModelForm):
    font_select = forms.ChoiceField(choices=get_available_fonts(), required=True)
    item_heading = forms.CharField(
        max_length=150,
        label="Item Set Heading",
        required=False,
    )

    class Meta:
        model = DataItemSetModel
        fields = ["position_x", "position_y", "font_size", "color"]


class ExportForm(forms.Form):
    EXPORT_CHOICES = [
        ("pdf", "PDF"),
        ("png", "PNG"),
        ("jpeg", "JPEG"),
    ]
    export_format = forms.ChoiceField(
        choices=EXPORT_CHOICES,
        widget=forms.RadioSelect,
        initial="png",
    )
