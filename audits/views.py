# audits/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Audit, Question, Response, Manager, User
from .forms import AuditForm, QuestionForm, ResponseForm
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from collections import defaultdict

def is_manager(user):
    try:
        return Manager.objects.get(user=user)
    except Manager.DoesNotExist:
        return None

@login_required
def dashboard(request):
    manager = is_manager(request.user)
    if manager:
        audits = Audit.objects.filter(manager=manager)
        responses_by_audit = defaultdict(list)
        responses = Response.objects.filter(question__audit__manager=manager)
        
        for response in responses:
            responses_by_audit[response.question.audit.id].append(response)
        
        context = {
            'audits': audits,
            'responses_by_audit': responses_by_audit,
            'now': timezone.now(),
        }
        return render(request, 'audits/dashboard.html', context)
    else:
        return redirect('useraudit_list')
    
@login_required
def view_responses(request, audit_id):
    manager = is_manager(request.user)
    if not manager:
        raise PermissionDenied

    audit = get_object_or_404(Audit, id=audit_id)
    responses = Response.objects.filter(question__audit=audit)
    context = {
        'audit': audit,
        'responses': responses,
    }
    return render(request, 'audits/view_responses.html', context)

@login_required
def create_audit(request):
    manager = is_manager(request.user)
    if not manager:
        raise PermissionDenied
    
    if request.method == 'POST':
        form = AuditForm(request.POST)
        if form.is_valid():
            audit = form.save(commit=False)
            audit.manager = manager
            audit.save()
            return redirect('add_questions', audit_id=audit.id)
    else:
        form = AuditForm()
    return render(request, 'audits/create_audit.html', {'form': form})

@login_required
def add_questions(request, audit_id):
    manager = is_manager(request.user)
    if not manager:
        raise PermissionDenied
    
    audit = get_object_or_404(Audit, id=audit_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.audit = audit
            question.save()
            return redirect('add_questions', audit_id=audit.id)
    else:
        form = QuestionForm()
    questions = Question.objects.filter(audit=audit)
    return render(request, 'audits/add_questions.html', {'form': form, 'audit': audit, 'questions': questions})

@login_required
def audit_list(request):
    manager = is_manager(request.user)
    if manager:
        audits = Audit.objects.filter(manager__user=request.user)
    else:
        audits = Audit.objects.filter(assigned_user=request.user)
    return render(request, 'audits/audit_list.html', {'audits': audits})

@login_required
def assign_audit(request, audit_id):
    manager = is_manager(request.user)
    if not manager:
        raise PermissionDenied
    
    audit = get_object_or_404(Audit, id=audit_id)
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        user = get_object_or_404(User, id=user_id)
        audit.assigned_user = user
        audit.save()
        return redirect('audit_list')
    users = User.objects.exclude(manager__isnull=False)
    return render(request, 'audits/assign_audit.html', {'audit': audit, 'users': users})

@login_required
def submit_response(request, audit_id):
    audit = get_object_or_404(Audit, id=audit_id)
    if is_manager(request.user):
        raise PermissionDenied

    questions = Question.objects.filter(audit=audit)
    if request.method == 'POST':
        for question in questions:
            response_text = request.POST.get(f'response_text_{question.id}')
            response_image = request.FILES.get(f'response_image_{question.id}')
            Response.objects.create(
                question=question,
                user=request.user,
                response_text=response_text,
                response_image=response_image
            )
        audit.completed = True
        audit.save()
        return redirect('audit_list')
    return render(request, 'audits/submit_response.html', {'audit': audit, 'questions': questions})

@login_required
def user_audit_list(request):
    audits = Audit.objects.filter(assigned_user=request.user)
    return render(request, 'audits/useraudit_list.html', {'audits': audits})