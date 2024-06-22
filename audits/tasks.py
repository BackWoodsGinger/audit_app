# audits/tasks.py
from celery import shared_task
from django.utils import timezone
from .models import Audit
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

@shared_task
def regenerate_audits():
    now = timezone.now()
    logger.info("Running regenerate_audits task at %s", now)
    audits = Audit.objects.all()

    for audit in audits:
        logger.info("Processing audit: %s", audit.title)
        if audit.frequency == 'D' and now >= audit.next_due_date:
            audit.next_due_date += timedelta(days=1)
            audit.save()
            logger.info("Updated next_due_date for daily audit: %s to %s", audit.title, audit.next_due_date)
        elif audit.frequency == 'W' and now >= audit.next_due_date:
            audit.next_due_date += timedelta(weeks=1)
            audit.save()
            logger.info("Updated next_due_date for weekly audit: %s to %s", audit.title, audit.next_due_date)
        elif audit.frequency == 'M' and now >= audit.next_due_date:
            audit.next_due_date += timedelta(days=30)  # Roughly a month
            audit.save()
            logger.info("Updated next_due_date for monthly audit: %s to %s", audit.title, audit.next_due_date)
        elif audit.frequency == 'Y' and now >= audit.next_due_date:
            audit.next_due_date += timedelta(days=365)  # Roughly a year
            audit.save()
            logger.info("Updated next_due_date for yearly audit: %s to %s", audit.title, audit.next_due_date)