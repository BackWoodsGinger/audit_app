# audits/forms.py
from django import forms
from .models import Audit, Question, Response

class AuditForm(forms.ModelForm):
    class Meta:
        model = Audit
        fields = ['title', 'description', 'frequency']

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['task_description', 'why', 'expected_result']

class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ['response_text', 'response_image']