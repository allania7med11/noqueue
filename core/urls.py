from django.urls import path
from .views import QueueListCreateView, QueueCitationListCreateView

urlpatterns = [
    path('queues/', QueueListCreateView.as_view(), name='queue-list-create'),
    path('queuecitations/', QueueCitationListCreateView.as_view(), name='queue-citation-list-create'),
    # Add more URL patterns as needed
]