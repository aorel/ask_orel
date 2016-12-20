from __future__ import print_function

from django.core.management.base import BaseCommand
from django.core.cache import cache

from django.db.models import Count
from askme.models import Tag

from datetime import datetime, timedelta


class Command(BaseCommand):

    def handle(self, *args, **options):
        s = '[' + str(datetime.now()) + '] ' + 'askme_popular_tags'
        print(s)

        last_month = datetime.today() - timedelta(days=10)  # USE_TZ = False
        # tags_set = Tag.objects.annotate(num=Count('question')).order_by('-num')[:5]
        tags_set = Tag.objects.filter(question__date__gte=last_month).annotate(num=Count('question')).order_by('-num')

        tags = []
        for tag in tags_set:
            # tags.append(str(tag.name)+'('+str(tag.num)+')')
            tags.append([
                str(tag.name),
                str(tag.num),
            ])
        print(tags)
        for key, value in tags:
            print(key, value)

        # cache.set('popular_tags', ['tag1', 'tag2', 'tag3', 'tag4', 'tag5', ])
        cache.set('popular_tags', tags, 30)
