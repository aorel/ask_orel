from django.core.management.base import BaseCommand
from askme.models import User, Profile, Tag, Question

class Command(BaseCommand):

    def handle(self, *args, **options):
        print("delete tags...")
        Tag.objects.filter(name__startswith='_').delete()

        print("delete users and profiles...")
        User.objects.filter(username__startswith='_').delete()
        Profile.objects.filter(user__username__startswith='_').delete()

        print("delete questions, questions votes, answers, answers votes...")
        Question.objects.filter(title__startswith='_').delete()
