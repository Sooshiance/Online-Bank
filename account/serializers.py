from rest_framework.serializers import ModelSerializer

from .models import BankAccount


class AccountSerializer(ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ('user', 'accounttype', 'code_account', 'current_asset')
        
        def create(self, validated_data):
            return BankAccount.objects.create_user(**validated_data)
        
        def update(self, validated_data):
            return BankAccount.objects.update(**validated_data)
