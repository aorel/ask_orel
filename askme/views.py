from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponse, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from models import Question

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


def test(request):
    return render(request, 'test.html')


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
    question_by_id = get_object_or_404(Question, pk=question_id)
    context['question'] = question_by_id
    return render(request, 'question.html', context)

    '''try:
        question_by_id = Question.objects.get(id=question_id)
        context['question'] = question_by_id
        return render(request, 'question.html', context)
    except Question.DoesNotExist:
        raise Http404("No Question matches the given query.")'''


def questions(request, page=1):
    new_questions = Question.objects.new()
    context['page'] = my_paginator(new_questions, page)
    return render(request, 'questions.html', context)


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def ask(request):
    return render(request, 'ask.html', context)
