from locale import currency

from rest_framework import serializers
from .models import Wallet

class WalletListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['uuid', 'currency', 'balance']

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['currency', 'balance']

class OperationSerializer(serializers.Serializer):
    operationType = serializers.ChoiceField(choices=['DEPOSIT', 'WITHDRAW'])
    amount = serializers.FloatField()