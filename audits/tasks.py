# audits/tasks.py
from celery import shared_task
from django.core.management import call_command

@shared_task
def regenerate_audits():
    call_command('regenerate_audits')