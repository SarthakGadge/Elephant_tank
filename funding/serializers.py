from rest_framework.serializers import ModelSerializer
from .models import Funding


class FundingSerializers(ModelSerializer):
    class Meta:
        model = Funding
        fields = ['id', 'amount', 'transaction_id', 'funded_at', 'idea_id_id',
                  'investor_id', 'payment_status', 'razorpay_order_id', 'razorpay_payment_id']
