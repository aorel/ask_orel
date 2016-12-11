# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone

from django.template.defaultfilters import truncatechars


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


def add_vote(current_object, exist, new_choice, old_vote):
    if exist is True:
        if old_vote.vote == new_choice:
            print "vote delete"
            old_vote.delete()
            if new_choice is True:
                current_object.vote_sum -= 1
                current_object.save()
            elif new_choice is False:
                current_object.vote_sum += 1
                current_object.save()
            else:
                print "[ERROR] if/elif/ELSE"
        else:
            print "vote swap"
            old_vote.vote = new_choice
            old_vote.save()
            if new_choice is True:
                current_object.vote_sum += 2
                current_object.save()
            elif new_choice is False:
                current_object.vote_sum -= 2
                current_object.save()
            else:
                print "[ERROR] if/elif/ELSE"
    else:
        if new_choice is True:
            current_object.vote_sum += 1
            current_object.save()
        elif new_choice is False:
            current_object.vote_sum -= 1
            current_object.save()
        else:
            print "[ERROR] if/elif/ELSE"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,)
    about = models.TextField(verbose_name=u'About', blank=True, null=True,)
    avatar = models.ImageField(blank=True, null=True,
                               upload_to=user_directory_path,
                               height_field="avatar_height",
                               width_field="avatar_width",)
    avatar_height = models.IntegerField(blank=True, null=True,)
    avatar_width = models.IntegerField(blank=True, null=True,)

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

    def vote(self, question_id, user, vote_choice):
        question = self.get(pk=question_id)
        vote = question.questionvote_set.filter(user=user)
        if vote:
            if len(vote) > 1:
                print "[ERROR] QuestionManager.like(): len(vote) > 1"
            add_vote(question, True, vote_choice, vote[0])
        else:
            print "vote new"
            new_vote = QuestionVote.objects.create(
                question=question,
                user=user,
                vote=vote_choice,
            )
            add_vote(question, False, vote_choice, False)


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
    vote_sum = models.IntegerField(
        default=0,
        verbose_name=u'Vote sum',
    )

    objects = QuestionManager()

    class Meta:
        verbose_name = u'Question'
        verbose_name_plural = u'Questions'

    def __unicode__(self):
        # return self.title
        return self.title + " (" + unicode(self.user) + ")"


class QuestionVote(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    VOTE_CHOICES = (
        (None, "Neutral"),
        (True, "Like"),
        (False, "Dislike")
    )
    vote = models.NullBooleanField(choices=VOTE_CHOICES, verbose_name=u'Vote')

    class Meta:
        verbose_name = u'QuestionVote'
        verbose_name_plural = u'QuestionVotes'
        unique_together = ('question', 'user',)

    def __unicode__(self):
        return unicode(self.user)


class AnswerManager(models.Manager):
    def vote(self, answer_id, user, vote_choice):
        answer = self.get(pk=answer_id)
        vote = answer.answervote_set.filter(user=user)
        if vote:
            if len(vote) > 1:
                print "[ERROR] QuestionManager.like(): len(vote) > 1"
            add_vote(answer, True, vote_choice, vote[0])
        else:
            print "vote new"
            new_vote = AnswerVote.objects.create(
                answer=answer,
                user=user,
                vote=vote_choice,
            )
            add_vote(answer, False, vote_choice, False)

    def correct(self, answer_id, user):
        answer = self.get(pk=answer_id)
        if answer.question.user == user:
            question = answer.question
            correct_answers = question.answer_set.filter(correct=True)
            for correct_answer in correct_answers:
                correct_answer.correct = False
                correct_answer.save()

            if answer.correct is True:
                answer.correct = False
                answer.save()
            elif answer.correct is False:
                answer.correct = True
                answer.save()
            else:
                print "[ERROR] if/elif/ELSE"


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
    vote_sum = models.IntegerField(
        default=0,
        verbose_name=u'Vote sum',
    )
    correct = models.BooleanField(verbose_name=u'Correct', default=False)

    objects = AnswerManager()

    @property
    def some_text(self):
        return truncatechars(self.text, 50)

    class Meta:
        verbose_name = u'Answer'
        verbose_name_plural = u'Answers'

    def __unicode__(self):
        return unicode(self.question) + " (" + unicode(self.user) + ")"


class AnswerVote(models.Model):
    answer = models.ForeignKey(
        Answer,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )
    VOTE_CHOICES = (
        (None, "Neutral"),
        (True, "Like"),
        (False, "Dislike")
    )
    vote = models.NullBooleanField(choices=VOTE_CHOICES, verbose_name=u'Vote')

    class Meta:
        verbose_name = u'AnswerVote'
        verbose_name_plural = u'AnswerVotes'
        unique_together = ('answer', 'user',)

    def __unicode__(self):
        return unicode(self.user)

