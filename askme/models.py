# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone

from django.template.defaultfilters import truncatechars

# Create your models here.

'''
class ArticleManager(models.Manager):
    def published(self):
        return self.filter(is_published=True)


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name=u'Заголовок')
    text = models.TextField(verbose_name=u'Текст')
    is_published = models.BooleanField(default=False, verbose_name=u'Опубликована')
    author = models.ForeignKey('Author')

    object = ArticleManager()

    class Meta:
        verbose_name = u'Статья'
        verbose_name_plural = u'Статьи'

    def __unicode__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=255, verbose_name=u'Имя')
    birthday = models.DateField(null=False, blank=False, verbose_name=u'Дата рождения')

    class Meta:
        verbose_name = u'Автор'
        verbose_name_plural = u'Авторы'

    def __unicode__(self):
        return self.name
'''


class ProfileManager(models.Manager):
    def _test(self):
        pass


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    about = models.TextField(verbose_name=u'About', blank=True, null=True)
    # avatar = models.ImageField(blank=True, null=True)

    objects = ProfileManager()

    class Meta:
        verbose_name = u'Profile'
        verbose_name_plural = u'Profiles'

    def __unicode__(self):
        return unicode(self.user)


class TagManager(models.Manager):
    def _test(self):
        pass


class Tag(models.Model):
    name = models.CharField(verbose_name=u'Tag', max_length=255,  unique=True)

    objects = TagManager()

    class Meta:
        verbose_name = u'Tag'
        verbose_name_plural = u'Tags'

    def __unicode__(self):
        return self.name


class QuestionManager(models.Manager):
    def get_by_id(self, question_id):
        # a = Answer.objects.filter(question=q_id)
        return self.get(id=question_id)

    def get_by_tag(self, tag_name):
        return self.filter(tags__name=tag_name)

    def new(self):
        return self.order_by('-date')

    def best(self):
        return self.order_by('-votes')


class Question(models.Model):
    title = models.CharField(verbose_name=u'Title', max_length=255,)
    text = models.TextField(verbose_name=u'Text',)
    date = models.DateTimeField(verbose_name=u'Date', default=timezone.now)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    votes = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag,)

    objects = QuestionManager()

    class Meta:
        verbose_name = u'Question'
        verbose_name_plural = u'Questions'

    def __unicode__(self):
        return self.title


class AnswerManager(models.Manager):
    def get_by_id(self, q_id):
        return self.filter(question=q_id)


class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    text = models.TextField(verbose_name=u'Text')
    date = models.DateTimeField(verbose_name=u'Date', default=timezone.now)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    votes = models.IntegerField()

    objects = AnswerManager()

    @property
    def custom_admin_display(self):
        return truncatechars(self.text, 50) + " (" + truncatechars(unicode(self.question), 50) + ')'

    class Meta:
        verbose_name = u'Answer'
        verbose_name_plural = u'Answers'

    def __unicode__(self):
        return self.text
