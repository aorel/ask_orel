# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone

from django.template.defaultfilters import truncatechars


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    about = models.TextField(verbose_name=u'About', blank=True, null=True)
    # avatar = models.ImageField(blank=True, null=True)

    class Meta:
        verbose_name = u'Profile'
        verbose_name_plural = u'Profiles'

    def __unicode__(self):
        return unicode(self.user)


class Tag(models.Model):
    name = models.CharField(verbose_name=u'Tag', max_length=255,  unique=True)

    class Meta:
        verbose_name = u'Tag'
        verbose_name_plural = u'Tags'

    def __unicode__(self):
        return self.name


class QuestionManager(models.Manager):
    def get_by_tag(self, tag_name):
        return self.filter(tags__name=tag_name)

    def new(self):
        return self.order_by('-date')

    def best(self):
        return self.annotate(num_votes=models.Count('questionvote')).order_by('-num_votes')[:5]


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
    tags = models.ManyToManyField(Tag,)

    objects = QuestionManager()

    class Meta:
        verbose_name = u'Question'
        verbose_name_plural = u'Questions'

    def __unicode__(self):
        return self.title


class QuestionVote(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = u'QuestionVote'
        verbose_name_plural = u'QuestionVotes'
        unique_together = ('question', 'user',)

    def __unicode__(self):
        return unicode(self.user)


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

    objects = AnswerManager()

    @property
    def custom_admin_display(self):
        return truncatechars(self.text, 50) + " (" + truncatechars(unicode(self.question), 50) + ')'

    class Meta:
        verbose_name = u'Answer'
        verbose_name_plural = u'Answers'

    def __unicode__(self):
        return self.text


class AnswerVote(models.Model):
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = u'AnswerVote'
        verbose_name_plural = u'AnswerVotes'
        unique_together = ('answer', 'user',)

    def __unicode__(self):
        return unicode(self.user)

