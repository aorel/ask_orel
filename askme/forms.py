from django import forms

from django.contrib import auth
from django.contrib.auth.models import User
from models import Question, Answer, Profile


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', ]

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'type': 'password',
        })
        self.user_cache = None

    def clean(self):
        print 'clean'
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        self.user_cache = auth.authenticate(
            username=username,
            password=password,
        )
        if self.user_cache is not None:
            pass
        else:
            raise forms.ValidationError('Login or password incorrect')


class SignupForm(forms.ModelForm):
    repeat_password = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', ]

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'type': 'password',
        })
        self.fields['repeat_password'].widget = forms.PasswordInput()
        self.fields['repeat_password'].widget.attrs.update({
            'class': 'form-control',
            'type': 'password',
        })

    def clean_username(self):
        print 'clean_username'
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("A user with that username already exists.")

    def clean(self):
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')

        if password and password != repeat_password:
            raise forms.ValidationError("Passwords don't match")
        # return self.cleaned_data

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            profile = Profile(
                user=user,
                about='',
            )
            profile.save()

        return user


class ProfileForm(forms.ModelForm):
    repeat_password = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', ]

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'type': 'password',
        })
        self.fields['repeat_password'].widget = forms.PasswordInput()
        self.fields['repeat_password'].widget.attrs.update({
            'class': 'form-control',
            'type': 'password',
        })

    def clean_username(self):
        print 'clean_username'
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("A user with that username already exists.")

    def clean(self):
        password = self.cleaned_data.get('password')
        repeat_password = self.cleaned_data.get('repeat_password')

        if password and password != repeat_password:
            raise forms.ValidationError("Passwords don't match")
        # return self.cleaned_data

    def save(self, commit=True):
        user = super(ProfileForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            profile = Profile(
                user=user,
                about='',
            )
            profile.save()

        return user


class AskForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags', ]

    def __init__(self, *args, **kwargs):
        super(AskForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['text'].widget.attrs.update({
            'class': 'form-control askme-textarea',
            'rows': 5,
        })
        self.fields['tags'].widget.attrs.update({
            'class': 'form-control'
        })


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', ]

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({
            'placeholder': 'Type your answer',
            'class': 'form-control askme-textarea',
            'rows': 5,
        })
