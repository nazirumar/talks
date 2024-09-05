from django.urls import path
from . import views

urlpatterns = [
    path('start-one-to-one/<int:invitee_id>/', views.start_one_to_one_call, name='start_one_to_one_call'),
    path('start-group/', views.start_group_call, name='start_group_call'),
    path('join/<uuid:call_id>/', views.join_call, name='join_call'),
    path('invite/accept/<uuid:invite_id>/', views.accept_invitation, name='accept_invitation'),
    path('call/<uuid:call_id>/', views.call_view, name='call_view'),  # Add this line




]
