from django.urls import path
from .views import SavingsAccountCreateView, SavingsAccountsListView, SavingsAccountSearchAPI

urlpatterns = [
    path('savings/create/', SavingsAccountCreateView.as_view(), name='savings-create'),
    path('savings/', SavingsAccountsListView.as_view(), name='savings-list'),
    path('savings/search/', SavingsAccountSearchAPI.as_view(), name='savings-search'),
]
