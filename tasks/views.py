from django.shortcuts import render
from . models import Task
from . serializers import TaskSerializer
from rest_framework import viewsets, permissions
from rest_framework.response import Response
# Create your views here.
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)