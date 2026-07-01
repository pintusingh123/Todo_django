from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from tudoapp.models import Todo


class Command(BaseCommand):
    help = "Delete tasks older than 15 days from trash"

    def handle(self, *args, **kwargs):

        expiry_date = timezone.now() - timedelta(days=15)

        deleted_count = Todo.objects.filter(
            is_deleted=True,
            deleted_at__lte=expiry_date
        ).delete()[0]

        self.stdout.write(
            f"{deleted_count} old trash tasks permanently deleted."
        )