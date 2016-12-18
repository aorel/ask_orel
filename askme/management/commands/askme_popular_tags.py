from __future__ import print_function

from django.core.management.base import BaseCommand
from askme.models import Tag


class Command(BaseCommand):

    def handle(self, *args, **options):

        print("calculation popular tags...")
        # self.annotate(num_votes=models.Count('questionvote')).order_by('-num_votes')[:5]
        # tags = Tag.annotate
