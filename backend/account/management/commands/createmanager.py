from django.conf import settings
from django.core.management.base import BaseCommand
from account.models import User

class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            User.objects.create_superuser(email="0@gmail.com", username="0000000000", password="0000000000")
            print('Manager created.')
        else:
            print('Manager accounts can only be initialized if no Accounts exist.')
