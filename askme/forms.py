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
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
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
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("A user with that username already exists.")

    def clean(self):
        password = self.cleaned_data['password']
        repeat_password = self.cleaned_data['repeat_password']

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


class ProfileUserForm(forms.ModelForm):
    new_password = forms.CharField()
    repeat_new_password = forms.CharField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', ]

    def __init__(self, current_user, *args, **kwargs):
        super(ProfileUserForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['password'].label = 'Old password'
        self.fields['password'].required = False
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'type': 'password',
        })

        self.fields['new_password'].label = 'New password'
        self.fields['new_password'].required = False
        self.fields['new_password'].widget = forms.PasswordInput()
        self.fields['new_password'].widget.attrs.update({
            'class': 'form-control',
            'type': 'password',
        })

        self.fields['repeat_new_password'].label = 'Repeat new password'
        self.fields['repeat_new_password'].required = False
        self.fields['repeat_new_password'].widget = forms.PasswordInput()
        self.fields['repeat_new_password'].widget.attrs.update({
            'class': 'form-control',
            'type': 'password',
        })
        self.user_cache = None
        self.current_user = current_user

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            user = User.objects.get(username=username)
            if user.id == self.current_user.id:
                return user.username
            else:
                raise forms.ValidationError("A user with that username already exists.")
        except User.DoesNotExist:
            return username

    def clean(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        new_password = self.cleaned_data['new_password']
        repeat_new_password = self.cleaned_data['new_password']

        if password or new_password or repeat_new_password:
            self.user_cache = auth.authenticate(
                username=username,
                password=password,
            )
            if self.user_cache is not None:
                pass
            else:
                raise forms.ValidationError('Old password incorrect')

            if new_password and new_password != repeat_new_password:
                raise forms.ValidationError("Passwords don't match")
        # return self.cleaned_data

    def save(self, commit=True):
        username = self.cleaned_data["username"]
        email = self.cleaned_data["email"]
        new_password = self.cleaned_data["new_password"]

        if username:
            self.current_user.username = username
        if email:
            self.current_user.email = email
        if new_password:
            self.current_user.set_password(new_password)
        if commit:
            self.current_user.save()


class ProfileExtraForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['about', 'avatar', ]

    def __init__(self, current_user, *args, **kwargs):
        super(ProfileExtraForm, self).__init__(*args, **kwargs)
        self.fields['about'].widget.attrs.update({
            'class': 'form-control askme-textarea',
            'rows': 5,
        })
        self.user_cache = None
        self.current_user = current_user

    def save(self, commit=True):
        # profile = super(ProfileExtraForm, self).save(commit=False)

        about = self.cleaned_data["about"]
        avatar = self.cleaned_data["avatar"]

        profile = self.current_user.profile
        if about:
            profile.about = about

        if avatar:
            print "avatar"
            profile.avatar = avatar
        else:
            print "NOT avatar"

        if commit:
            profile.save()


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'text', 'tags', ]

    def __init__(self, current_user, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
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
        self.current_user = current_user

    def save(self, commit=True):
        question = super(QuestionForm, self).save(commit=False)
        question.user = self.current_user
        if commit:
            question.save()
        return question.id


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', ]

    def __init__(self, current_user, question_id, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['text'].widget.attrs.update({
            'placeholder': 'Type your answer',
            'class': 'form-control askme-textarea',
            'rows': 5,
        })
        self.current_user = current_user
        self.question_id = question_id
        self.question = None

    def clean(self):
        try:
            self.question = Question.objects.get(id=self.question_id)
        except Question.DoesNotExist:
            raise forms.ValidationError("Question does not exist")

    def save(self, commit=True):
        answer = super(AnswerForm, self).save(commit=False)
        print answer
        answer.user = self.current_user
        answer.question = self.question
        if commit:
            answer.save()
