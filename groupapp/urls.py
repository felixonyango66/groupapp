from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register-group/', views.register_group, name='register_group'),
    path('login/', views.login_group, name='login_group'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('milestones/', views.milestones, name='milestones'),
    path('group-photos/', views.group_photos, name='group_photos'),
    path('announcements/', views.announcements, name='announcements'),
    path('teaching-platform/', views.teaching_platform, name='teaching_platform'),
    path('training-platform/', views.training_platform, name='training_platform'),
    path('missions/', views.missions, name='missions'),
    path('members/', views.members, name='members'),
    path('members/', views.members, name='members'),
    path('visions/', views.visions, name='visions'),
    path('feedback/', views.feedbacks, name='feedbacks'),
    path('settings/', views.settings, name='settings'),
    path('funding-records/', views.funding_records, name='funding_records'),
    path('funding-records/', views.funding_records, name='funding_records'),
    path('logout/', views.logout_group, name='logout'),
    path('events/', views.events, name='events'),
    path('notifications/', views.notifications, name='notifications'),
    path('documents/', views.documents, name='documents'),
    path('request-reset/', views.request_reset, name='request_reset'),
    path('reset-password/<uuid:token>/', views.reset_password, name='reset_password'),
    path('ai/', views.ai_assistant, name='ai_assistant'),

]   