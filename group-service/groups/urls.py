from django.urls import path
from .views import (
    GroupCreationView,
    GroupJoinView,
    GroupLeaveView,
    GroupListView,
    GroupDetailView,
)

urlpatterns = [
    path('groups/create/', GroupCreationView.as_view(), name='group-create'),
    path('groups/join/', GroupJoinView.as_view(), name='group-join'),
    path('groups/leave/', GroupLeaveView.as_view(), name='group-leave'),
    path('groups/', GroupListView.as_view(), name='group-list'),
    path('groups/<uuid:group_id>/', GroupDetailView.as_view(), name='group-detail'),
]