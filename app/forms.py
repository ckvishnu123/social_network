from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from api.models import Posts, Comments

# in user creation form password hashig and other functionalities 
# will be done automatically
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password1",
                  "password2"]


# login doesn't need any action so here just forms.Form is enough
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()


class PostForm(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['title', 'image']

        widgets = {
            "title": forms.Textarea(attrs={
                "class": "form-control border border-top-0 border-start-0 border-end-0", "rows":5}),
            "image": forms.FileInput(attrs={"class": "form-select"})
        }



        