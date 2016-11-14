from django.core.management.base import BaseCommand
from askme.models import User, Profile, Tag, Question, Answer

import random

my_tags = ['html', 'css', 'javascript', 'django', 'flask', 'cpp', 'python', 'go', 'rust']
my_users = ['Pupkin', 'John Doe', 'Batman', 'Homer', 'Bender', 'Yoda']

test_tags = []
for i in my_tags:
    tag_name = '_{0}'.format(i)
    test_tags.append(tag_name)

test_users = []
for i in my_users:
    user_name = '_{0}'.format(i)
    test_users.append(user_name)


test_questions = []
for i in range(1, 11):
    one_question = dict()
    one_question['id'] = i
    one_question['title'] = '_Test question {0}'.format(i)
    one_question['text'] = "_{0} Lorem Ipsum  is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book.".format(i)

    one_question_answers = list()
    for j in range(1, 3):
        one_question_answer = dict()
        one_question_answer['id'] = '{0}_{1}'.format(i,j)
        one_question_answer['text'] = "_{0} @{1} It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.".format(i,j)
        one_question_answer['date'] = '{0}'.format(random.randint(1, 30))
        one_question_answer['votes'] = '{0}'.format(random.randint(1, 50))

        one_question_answers.append(one_question_answer)
    one_question['answers'] = one_question_answers

    one_question['date'] = '{0}'.format(random.randint(1, 30))
    one_question['votes'] = '{0}'.format(random.randint(1, 50))
    one_question['tags'] = ['tag1', 'tag2', 'tag3', 'tag4', 'tag5']
    test_questions.append(one_question)


class Command(BaseCommand):

    def handle(self, *args, **options):

        print("write tags...")
        for test_tag in test_tags:
            if Tag.objects.filter(name=test_tag).exists():
                pass
            else:
                tag = Tag(name=test_tag)
                tag.save()

        print("write users and profiles...")
        for test_user in test_users:
            if User.objects.filter(username=test_user).exists():
                pass
            else:
                user = User(
                    username=test_user,
                    first_name='test_first_name',
                    last_name='test_last_name',
                    email='test_email',
                    password='test',
                )
                user.save()

                profile = Profile(
                    user=user,
                    about='test_about'+user.username,
                )
                profile.save()

        print("write questions and answers...")
        for test_question in test_questions:
            if Question.objects.filter(title=test_question.get('title')).exists():
                pass
            else:
                random_question_user = random.choice(User.objects.filter(username__startswith='_'))
                # print random_question_user, random_question_user.id
                question = Question(
                    title=test_question.get('title'),
                    text=test_question.get('text'),
                    # data -> auto generated
                    user=random_question_user,
                    votes=random.randint(1, 50),
                    # tag=random.choice(test_tags),
                )
                question.save()
                random_tag = random.choice(Tag.objects.filter(name__startswith='_'))
                question.tags.add(random_tag)

                for test_answer in test_question.get('answers'):
                    random_answer_user = random.choice(User.objects.filter(username__startswith='_'))
                    answer = Answer(
                        question=question,
                        text=test_answer.get('text'),
                        # data -> auto generated
                        user=random_answer_user,
                        votes=random.randint(1, 10),
                    )
                    answer.save()
