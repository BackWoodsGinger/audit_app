# audits/admin.py
from django.contrib import admin
from .models import Manager, Question, Audit, Response

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['user']

@admin.register(Audit)
class AuditAdmin(admin.ModelAdmin):
    list_display = ['title', 'manager', 'frequency', 'next_due_date']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['audit', 'task_description', 'why', 'expected_result']

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['question', 'user', 'response_text', 'created_at']