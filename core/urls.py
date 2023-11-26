from django.urls import path, re_path
from .views import CurrentTicketView, QueueListCreateView, QueueCitationListCreateView, UserRegistrationView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('queues/', QueueListCreateView.as_view(), name='queue-list-create'),
    path('queuecitations/', QueueCitationListCreateView.as_view(), name='queue-citation-list-create'),
    re_path(r'^queuecitations/current_ticket/(?P<queue>[\w-]+)/$', CurrentTicketView.as_view(), name='current-ticket-slug'),
    # Add more URL patterns as needed
]