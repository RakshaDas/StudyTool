from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.Form):
    firstName = forms.CharField(required=True)
    lastName = forms.CharField(required=False)
    email = forms.EmailField(required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(),
    )
    cnf_password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        email = cleaned_data['email']
        username = cleaned_data['email'].split('@')[0]
        password = cleaned_data['password']
        cnf_password = cleaned_data['cnf_password']

        if len(password) < 8:
            self.add_error(
                'password', 'Password is too short. It must contain at least 8 character.')

        elif password != cnf_password:
            self.add_error(
                'cnf_password', "Password and Confirm Password must match!")

        if User.objects.filter(email=email).count():
            self.add_error('email', "This email address is already in use.")

        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        username = cleaned_data['email'].split('@')[0]
        user = User(username=username,
                    email=cleaned_data['email'],
                    first_name=cleaned_data['firstName'],
                    last_name=cleaned_data['lastName'])
        user.set_password(cleaned_data['password'])
        user.save()


class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=True
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data['email']
        password = cleaned_data['password']

        if not User.objects.filter(email=email).count():
            self.add_error('email', "Wrong email. Enter registered email.")

        elif not User.objects.filter(email=email).first().check_password(password):
            self.add_error(
                'password', 'Wrong passowrd. Enter correct password.')

        return cleaned_data


class EditAccountForm(forms.Form):
    firstName = forms.CharField(required=False)
    lastName = forms.CharField(required=False)
    email = forms.EmailField(required=False)
    image = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(EditAccountForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(EditAccountForm, self).clean()
        email = cleaned_data['email']

        if self.user and self.user.email == email:
            return cleaned_data

        if User.objects.filter(email=email).count():
            self.add_error('email', "This email address is already in use.")

        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        image = cleaned_data['image']
        if image and self.user.profile.image != image:
            self.user.profile.image = image
            self.user.profile.save()

        self.user.username = cleaned_data['email'].split('@')[0]
        self.user.email = cleaned_data['email']
        self.user.first_name = cleaned_data['firstName']
        self.user.last_name = cleaned_data['lastName']
        self.user.save()


class ChangePasswordForm(forms.Form):
    currentPassword = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())
    cnf_password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        currentPassword = cleaned_data['currentPassword']
        password = cleaned_data['password']
        cnf_password = cleaned_data['cnf_password']

        if not self.user.check_password(currentPassword):
            self.add_error(
                'currentPassword', 'Enter your correct password.')

        if len(password) < 8:
            self.add_error(
                'password', 'Password is too short. It must contain at least 8 character.')

        elif password != cnf_password:
            self.add_error(
                'cnf_password', "Password and Confirm Password must match!")

        return cleaned_data

    def save(self):
        cleaned_data = self.cleaned_data
        self.user.set_password(cleaned_data['password'])
        self.user.save()
