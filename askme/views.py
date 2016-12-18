# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from models import Question, QuestionVote, Answer
from forms import LoginForm, SignupForm, ProfileUserForm, ProfileExtraForm, QuestionForm, AnswerForm

import datetime
import random


def current_datetime(request):
    now = datetime.datetime.now()
    html = "<p>It is now %s.</p>" % now
    return HttpResponse(html)


def hello_world(request):
    data = '<p>Hello, world!</p>'\
        '<p>' + request.path + '</p>'\
        '<p>' + request.method + ' ' + request.META['QUERY_STRING'] + '</p>'
    return HttpResponse(data)


# -----------------------------------------------------------------------------


# TODO tag 'c++' regex error
popular_tags = ['html', 'css', 'javascript', 'django', 'flask', 'cpp', 'python', 'go', 'rust']
best_members = ['Pupkin', 'John Doe', 'Batman', 'Homer', 'Bender', 'Yoda']

context = dict()
context['popular_tags'] = popular_tags
context['best_members'] = best_members

questions_list = []
for i in range(1, 51):
    one_question = dict()
    one_question['id'] = i
    one_question['title'] = 'Test question {0}'.format(i)
    one_question['text'] = "#{0} Lorem Ipsum  is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.".format(i)

    one_question_answers = list()
    for j in range(1, 3):
        one_question_answer = dict()
        one_question_answer['id'] = '{0}_{1}'.format(i, j)
        one_question_answer['text'] = "#{0} @{1} It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.".format(i,j)
        one_question_answer['meta'] = {
            'user': 'user{0}'.format(j),
            'date': '{0}'.format(random.randint(1, 30)),
            'rank': '{0}'.format(random.randint(1, 50)),
        }
        one_question_answers.append(one_question_answer)
    one_question['answers'] = one_question_answers

    one_question['meta'] = {
        'user': 'user{0}'.format(i),
        'date': '{0}'.format(random.randint(1, 30)),
        'answers': '{0}'.format(random.randint(1, 10)),
        'rank': '{0}'.format(random.randint(1, 50)),
        }
    one_question['tags'] = ['tag1', 'tag2', 'tag3', 'tag4', 'tag5']
    questions_list.append(one_question)


def my_paginator(objects_list, page, objects_per_page=10):
    paginator = Paginator(objects_list, objects_per_page)
    try:
        objects_on_page = paginator.page(page)
    except PageNotAnInteger:
        objects_on_page = paginator.page(1)
    except EmptyPage:
        objects_on_page = paginator.page(paginator.num_pages)
    return objects_on_page


def my_question_search(q_id):
    return filter(lambda qn: qn['id'] == q_id, questions_list)


def user_vote_dict(v):
    d = {}
    if v:
        d['like'] = 'askme-btn-like'
        d['dislike'] = ''
    else:
        d['like'] = ''
        d['dislike'] = 'askme-btn-dislike'
    return d

# -----------------------------------------------------------------------------


def best(request, page=1):
    best_questions = Question.objects.best()
    context['page'] = my_paginator(best_questions, page)
    return render(request, 'best.html', context)


def tag(request, tag_name, page=1):
    context['tag_name'] = tag_name
    questions_by_tag = Question.objects.get_by_tag(tag_name)
    context['page'] = my_paginator(questions_by_tag, page)
    return render(request, 'tag.html', context)


def question(request, question_id):
    if request.POST:
        form = AnswerForm(request.user, question_id, request.POST)
        if form.is_valid():
            print "question POST valid"
            new_answer = form.custom_save()
            new_answer.notify()
            return redirect(reverse('question', kwargs={'question_id': question_id}) + '#id_text')
    else:
        question_by_id = get_object_or_404(Question, pk=question_id)
        context['question'] = question_by_id

        if request.user.is_authenticated():
            q = context['question']
            _a = q.answer_set.all()

            context['user_question_vote'] = {}
            user_vote = q.questionvote_set.filter(user=request.user)
            if user_vote:
                if len(user_vote) > 1:
                    print "ERROR in user_vote"
                context['user_question_vote'][user_vote[0].question] = user_vote_dict(user_vote[0].vote)

            context['user_answer_vote'] = {}
            for a in _a:
                user_vote = a.answervote_set.filter(user=request.user)
                if user_vote:
                    if len(user_vote) > 1:
                        print "ERROR in user_vote"
                    context['user_answer_vote'][user_vote[0].answer] = user_vote_dict(user_vote[0].vote)
        form = AnswerForm(request.user, question_id)
    context['form'] = form
    return render(request, 'question.html', context)


def questions(request, page=1):
    new_questions = Question.objects.new()
    context['page'] = my_paginator(new_questions, page)

    if request.user.is_authenticated():
        _q = context['page']

        context['user_question_vote'] = {}
        for q in _q:
            user_vote = q.questionvote_set.filter(user=request.user)
            if user_vote:
                if len(user_vote) > 1:
                    print "ERROR in user_vote"
                context['user_question_vote'][user_vote[0].question] = user_vote_dict(user_vote[0].vote)
    return render(request, 'questions.html', context)


def login(request):
    next_page = request.GET.get('next')
    if next_page:
        print 'login next_page: ' + str(next_page)

    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            auth.login(request, form.user_cache)

            if next_page:
                return redirect(next_page)
            return redirect("/")
        else:
            pass
    else:
        form = LoginForm
    context['form'] = form
    return render(request, 'login.html', context)


def logout(request):
    next_page = request.GET.get('next')
    print 'logout next_page: ' + str(next_page)

    auth.logout(request)
    if next_page:
        return redirect(next_page)
    return redirect("/")


def signup(request):
    if request.POST:
        form = SignupForm(request.POST)
        if form.is_valid():
            print 'ok'
            form.save()
            user = auth.authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            auth.login(request, user)
            return redirect("/")
        else:
            print 'error'
            pass
    else:
        form = SignupForm
    context['form'] = form
    return render(request, 'signup.html', context)


@login_required
def profile(request):
    if request.user.profile.avatar:
        print request.user.profile.avatar.url

    if request.method == 'POST':
        form_user = ProfileUserForm(request.user, request.POST)
        form_extra = ProfileExtraForm(request.user, request.POST, request.FILES)

        print "is_multipart: " + str(form_extra.is_multipart())

        if form_user.is_valid() and form_extra.is_valid():
            form_user.save()
            form_extra.custom_save()
            auth.update_session_auth_hash(request, request.user)
            return redirect(reverse('profile'))
    else:
        form_user = ProfileUserForm(
            request.user,
            initial={
                'username': request.user.username,
                'email': request.user.email
            }
        )
        form_extra = ProfileExtraForm(
            request.user,
            initial={
                'about': request.user.profile.about,
                'avatar': request.user.profile.avatar,
            }
        )
    context['forms'] = (form_user, form_extra, )
    return render(request, 'profile.html', context)


@login_required
def ask(request):
    if request.POST:
        form = QuestionForm(request.user, request.POST)
        if form.is_valid():
            new_question = form.custom_save()
            return redirect(reverse('question', kwargs={'question_id': new_question}))
    else:
        form = QuestionForm(request.user)
    context['form'] = form
    return render(request, 'ask.html', context)


def vote(request):
    if request.POST:
        object_id = request.POST.get('id')
        object_type = request.POST.get('type')
        if object_id and object_type:
            json_response = {}
            if object_type == "question-like":
                json_response['action'] = Question.objects.vote(object_id, request.user, True)
                json_response['action']['type'] = 'like'
            elif object_type == "question-dislike":
                json_response['action'] = Question.objects.vote(object_id, request.user, False)
                json_response['action']['type'] = 'dislike'
            elif object_type == "answer-like":
                json_response['action'] = Answer.objects.vote(object_id, request.user, True)
                json_response['action']['type'] = 'like'
            elif object_type == "answer-dislike":
                json_response['action'] = Answer.objects.vote(object_id, request.user, False)
                json_response['action']['type'] = 'dislike'
            else:
                return JsonResponse({"status": "error: wrong type"})

            json_response['status'] = 'ok'
            return JsonResponse(json_response)
        else:
            return JsonResponse({"status": "error: empty id or type"})
    return JsonResponse({"status": "error: something wrong"})


def correct(request):
    if request.POST:
        object_id = request.POST.get('id')
        object_type = request.POST.get('type')
        if object_id and object_type:
            if object_type == "answer-correct":
                Answer.objects.correct(object_id, request.user)
            else:
                return JsonResponse({"status": "error: wrong type"})
            return JsonResponse({"status": "ok"})
        else:
            return JsonResponse({"status": "error: empty id or type"})
    return JsonResponse({"status": "error: something wrong"})
