# audits/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_audit, name='create_audit'),
    path('add_questions/<int:audit_id>/', views.add_questions, name='add_questions'),
    path('', views.audit_list, name='audit_list'),
    path('respond/<int:audit_id>/', views.submit_response, name='submit_response'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('assign_audit/<int:audit_id>/', views.assign_audit, name='assign_audit'),
    path('useraudit_list/', views.user_audit_list, name='useraudit_list'),
    path('view_responses/<int:audit_id>/', views.view_responses, name='view_responses'),
]