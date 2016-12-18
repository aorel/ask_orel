from __future__ import print_function

from django.core.management.base import BaseCommand
from askme.models import Question, Answer


class Command(BaseCommand):

    def handle(self, *args, **options):

        print("calculation best members...")
