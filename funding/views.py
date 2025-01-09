from .models import Funding, IdeaSubmission
from django.http import JsonResponse
from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest
from django.conf import settings
import razorpay
from rest_framework.permissions import AllowAny
from .models import Funding
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from student.models import IdeaSubmission
from userauth.models import Investor


class VerifyPaymentView(View):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Extract data from request
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        # Fetch the funding instance
        try:
            funding = Funding.objects.get(razorpay_order_id=razorpay_order_id)
        except Funding.DoesNotExist:
            return HttpResponseBadRequest("Invalid order ID")

        # Razorpay client
        client = razorpay.Client(
            auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

        # Verify signature
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })
        except razorpay.errors.SignatureVerificationError:
            funding.payment_status = 'failed'
            funding.save()
            return JsonResponse({'status': 'failure', 'message': 'Payment verification failed'})

        # Update funding with payment details
        funding.razorpay_payment_id = razorpay_payment_id
        funding.payment_status = 'success'
        funding.save()

        return JsonResponse({'status': 'success', 'message': 'Payment verified successfully'})


class CreateFundingOrderView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # Extract data from the request
        investor_id = request.data.get('investor_id')
        idea_id = request.data.get('idea_id')
        amount = request.data.get('amount')

        # Validate input data
        if not idea_id:
            return JsonResponse({'error': 'idea_id is required'}, status=400)

        if not amount:
            return JsonResponse({'error': 'amount is required'}, status=400)

        try:
            # Validate idea_id to be an integer
            idea_id = int(idea_id)
        except ValueError:
            return JsonResponse({'error': 'Invalid idea_id, it must be an integer'}, status=400)

        try:
            # Ensure the idea exists
            idea_instance = get_object_or_404(IdeaSubmission, id=idea_id)
        except IdeaSubmission.DoesNotExist:
            return JsonResponse({'error': 'Idea not found'}, status=404)

        # Validate investor_id
        if not investor_id:
            return JsonResponse({'error': 'investor_id is required'}, status=400)

        try:
            # Ensure the investor exists in the database
            investor_instance = Investor.objects.get(id=investor_id)
        except Investor.DoesNotExist:
            return JsonResponse({'error': 'Investor not found'}, status=404)

        # Check if the amount is valid
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            return JsonResponse({'error': 'Invalid amount, it must be a positive number'}, status=400)

        # Create Funding instance with pending payment status
        funding = Funding.objects.create(
            investor_id=investor_instance.id,  # Make sure this is a valid ForeignKey instance
            idea_id=idea_instance,  # Corrected field name
            amount=amount,
            payment_status='pending'
        )

        # Razorpay client setup
        client = razorpay.Client(
            auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET)
        )

        # Create an order in Razorpay
        data = {
            'amount': int(amount * 100),  # Convert to paise
            'currency': 'INR',
            'receipt': funding.transaction_id,
            'payment_capture': 1,  # Auto-capture payment
        }

        try:
            razorpay_order = client.order.create(data=data)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

        # Update Funding with Razorpay order ID
        funding.razorpay_order_id = razorpay_order['id']
        funding.save()

        # Return order details
        return JsonResponse({
            'order_id': razorpay_order['id'],
            'razorpay_key': settings.RAZORPAY_API_KEY,
            'amount': amount,
            'currency': 'INR',
        })
