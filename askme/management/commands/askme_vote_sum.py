from __future__ import print_function

from django.core.management.base import BaseCommand
from askme.models import Question, Answer


class Command(BaseCommand):

    def handle(self, *args, **options):

        print("calculation question votes...", end=" ")
        new_questionsum_flag = False
        questions = Question.objects.all()
        for question in questions:
            questionvotes = question.questionvote_set.all()
            questionsum = 0
            for questionvote in questionvotes:
                if questionvote.vote is True:
                    questionsum += 1
                elif questionvote.vote is False:
                    questionsum -= 1
                else:
                    print()
                    print("[ERROR] questionvote.vote")
            if question.vote_sum != questionsum:
                new_questionsum_flag = True
                question.vote_sum = questionsum
                question.save()
        if new_questionsum_flag is True:
            print("new sum")
        else:
            print("ok")

        print("calculation answer votes...", end=" ")
        new_answersum_flag = False
        answers = Answer.objects.all()
        for answer in answers:
            answervotes = answer.answervote_set.all()
            answersum = 0
            for answervote in answervotes:
                if answervote.vote is True:
                    answersum += 1
                elif answervote.vote is False:
                    answersum -= 1
                else:
                    print()
                    print("[ERROR] answervote.vote")
            if answer.vote_sum != answersum:
                new_answersum_flag = True
                answer.vote_sum = answersum
                answer.save()
        if new_answersum_flag is True:
            print("new sum")
        else:
            print("ok")