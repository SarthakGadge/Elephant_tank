from django.urls import path
from .views import CreateFundingOrderView, VerifyPaymentView

urlpatterns = [
    path('create-order/', CreateFundingOrderView.as_view(), name='create_funding_order'),
    path('verify-payment/', VerifyPaymentView.as_view(), name='verify_payment'),
]
