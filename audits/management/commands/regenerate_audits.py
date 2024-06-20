# audits/management/commands/regenerate_audits.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from audits.models import Audit

class Command(BaseCommand):
    help = 'Regenerate audits based on their frequency'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        due_audits = Audit.objects.filter(next_due_date__lte=now)
        for audit in due_audits:
            audit.next_due_date = audit.calculate_next_due_date()
            audit.save()
            self.stdout.write(self.style.SUCCESS(f'Regenerated audit: {audit.title}'))