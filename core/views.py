from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Queue, QueueCitation
from .serializers import QueueSerializer, QueueCitationSerializer

class QueueListCreateView(generics.ListCreateAPIView):
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer
    permission_classes = [IsAuthenticated]

class QueueCitationListCreateView(generics.ListCreateAPIView):
    queryset = QueueCitation.objects.all()
    serializer_class = QueueCitationSerializer
    permission_classes = [IsAuthenticated]