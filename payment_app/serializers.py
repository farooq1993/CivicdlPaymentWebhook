from rest_framework import serializers
from .models import PaymentOrder
from django.core.exceptions import ValidationError  

class PayementOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentOrder
        fields = "__all__"

    def validate(self, data):
        if data['amount'] <= 0:
            raise ValidationError("Amount must be greater than zero.")
        return data 
