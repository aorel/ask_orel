from __future__ import print_function

from django.core.management.base import BaseCommand
from django.core.cache import cache

from django.db.models import Count
from askme.models import User

from datetime import datetime, timedelta


class Command(BaseCommand):

    def handle(self, *args, **options):
        s = '[' + str(datetime.now()) + '] ' + 'askme_best_members'
        print(s)

        last_month = datetime.today() - timedelta(days=10)  # USE_TZ = False
        members_question_set = User.objects.filter(question__date__gte=last_month).annotate(num=Count('question')).order_by('-num')
        members_answer_set = User.objects.filter(answer__date__gte=last_month).annotate(num=Count('answer')).order_by('-num')

        members_dict = {}
        for member in members_question_set:
            # members.append(str(member.username) + '(' + str(member.num) + ')')
            if member in members_dict:
                members_dict[member] += member.num
            else:
                members_dict[member] = member.num

        for member in members_answer_set:
            # members.append(str(member.username) + '(' + str(member.num) + ')')
            if member in members_dict:
                members_dict[member] += member.num
            else:
                members_dict[member] = member.num

        print(members_dict)
        members_list = sorted(members_dict, key=members_dict.get, reverse=True)
        print(members_list)

        members = []
        for member in members_list:
            members.append([
                str(member.username),
                str(members_dict[member]),
            ])
        print(members)
        for key, value in members:
            print(key, value)

        # cache.set('best_members', ['member1', 'member2', 'member3', 'member4', 'member5', ])
        cache.set('best_members', members, 30)
