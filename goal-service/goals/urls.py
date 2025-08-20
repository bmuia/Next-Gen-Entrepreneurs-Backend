from django.urls import path
from .views import GoalCreateView, GoalListView, GoalRetrieveUpdateView

urlpatterns = [
    path('goals/create/', GoalCreateView.as_view(), name='goal-create'),
    path('goals/', GoalListView.as_view(), name='goal-list'),
    path('goals/<int:pk>/', GoalRetrieveUpdateView.as_view(), name='goal-detail'),
]