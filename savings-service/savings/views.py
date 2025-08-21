from rest_framework import generics, status
from rest_framework.response import Response
from .models import SavingsAccount
from .serializers import SavingsAccountSerializer
from .authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.utils.dateparse import parse_datetime

# Create your views here.
class SavingsAccountCreateView(generics.CreateAPIView):
    queryset = SavingsAccount.objects.all()
    serializer_class = SavingsAccountSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(account_holder=self.request.user['user_id'])

class SavingsAccountsListView(generics.ListAPIView):
    queryset = SavingsAccount.objects.all()
    serializer_class = SavingsAccountSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]


    def get_queryset(self):
        return SavingsAccount.objects.all().filter(account_holder=self.request.user['user_id'])
        
class SavingsAccountSearchAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        from_date = request.query_params.get("from_date")
        end_date = request.query_params.get("end_date")

      
        if not from_date:
            return Response({"error": "from_date is required"}, status=400)

    
        from_date = from_date.strip()
        end_date = end_date.strip() if end_date else None

      
        from_date = parse_datetime(from_date)
        end_date = parse_datetime(end_date) if end_date else None

        if not from_date:
            return Response({"error": "Invalid from_date format. Use ISO8601 (e.g., 2025-08-21T15:39:30Z)."}, status=400)

      
        queryset = SavingsAccount.objects.filter(account_holder=request.user["user_id"])

        if end_date:
            queryset = queryset.filter(created_at__range=[from_date, end_date])
        else:
            queryset = queryset.filter(created_at__gte=from_date)

        serializer = SavingsAccountSerializer(queryset, many=True)
        return Response(serializer.data, status=200)