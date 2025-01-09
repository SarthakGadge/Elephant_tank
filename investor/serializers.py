from rest_framework.serializers import ModelSerializer
from userauth.models import Investor
from .models import InvestorFunding, InvestorInterest

class InvestorSerializer(ModelSerializer):
    class Meta:
        model = Investor
        fields = ["id", "full_name", "email", "phone_number", "role", "domain", "linked_url", "gender", "organisation", "is_active", "admin_approval"]
        

class InvestorInterestSerializer(ModelSerializer):
    class Meta:
        model = InvestorInterest
        fields = '__all__'
        depth = 1
        
class InvestorFundingSerializer(ModelSerializer):
    class Meta:
        model = InvestorFunding
        fields = '__all__'
        depth = 1
    