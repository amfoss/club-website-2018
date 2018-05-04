from django.core.management import BaseCommand

from attendance.models import SSIDName


class Command(BaseCommand):
    help = 'Generates a new ssid(need to run as a cron job everyday)'

    def handle(self, *args, **options):
        ssid_name, created = SSIDName.objects.get_or_create(id=1)
        ssid_name.generate_random_name()
        ssid_name.save()
        print(ssid_name.name)
