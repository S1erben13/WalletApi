from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import WalletSerializer, WalletListSerializer, OperationSerializer
from .models import Wallet


# Create your views here.
class WalletList(generics.ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletListSerializer


class WalletApi(generics.RetrieveAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_field = 'uuid'


class WalletOperation(APIView):
    def post(self, request, uuid):
        try:
            serializer = OperationSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            operation_type = serializer.validated_data['operationType']
            amount = serializer.validated_data['amount']
            wallet = Wallet.objects.select_for_update().get(uuid=uuid)
            if operation_type == 'DEPOSIT':
                wallet.deposit(amount)
            elif operation_type == 'WITHDRAW':
                wallet.withdraw(amount)

            return Response({"balance": wallet.balance}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Wallet.DoesNotExist:
            return Response({"error": "Wallet does not exist"}, status=status.HTTP_404_NOT_FOUND)
