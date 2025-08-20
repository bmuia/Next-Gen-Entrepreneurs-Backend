from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Goal
from .serializers import GoalSerializer
from rest_framework.permissions import IsAuthenticated
from .authentication import JWTAuthentication
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied


# Create your views here.

class GoalCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = GoalSerializer

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user['user_id'])
       
    
class GoalRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer

    def perform_update(self, serializer):
        serializer.save(user_id=self.request.user['user_id'])

    def get_object(self):
        obj = super().get_object()
        if obj.user_id != self.request.user['user_id']:
            raise PermissionDenied("You do not have permission to view this goal.")
        return obj

    
class GoalListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    serializer_class = GoalSerializer

    """
    View to list all goals for the authenticated user.
    """
    def get_queryset(self):
        return Goal.objects.filter(user_id=self.request.user['user_id'])
    