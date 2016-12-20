from django.core.management.base import BaseCommand
import datetime


class Command(BaseCommand):

    def handle(self, *args, **options):
        s = '[' + str(datetime.datetime.now()) + '] ' + 'test'
        print s
