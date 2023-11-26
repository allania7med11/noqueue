from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Queue, QueueCitation
from .serializers import QueueSerializer, QueueCitationSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import status

class QueueListCreateView(generics.ListCreateAPIView):
    serializer_class = QueueSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Queue.objects.filter(created_by=self.request.user)

class QueueCitationListCreateView(generics.ListCreateAPIView):
    serializer_class = QueueCitationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return QueueCitation.objects.filter(created_by=self.request.user)
    

class CurrentTicketView(APIView):
    serializer_class = QueueCitationSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, queue):
        queryset = QueueCitation.objects.filter(queue__slug=queue, created_by=request.user)  # You can customize this condition based on your state choices
        last_not_served_citation = queryset.order_by('-id').first()
        if last_not_served_citation:
            serializer = QueueCitationSerializer(last_not_served_citation)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)