import uuid
from django.db import models
from django.utils.timezone import now
from student.models import IdeaSubmission
from userauth.models import Investor


import uuid
from django.db import models
from django.utils import timezone


class Funding(models.Model):
    idea_id = models.ForeignKey(
        IdeaSubmission, on_delete=models.CASCADE, related_name='fundings')
    investor = models.ForeignKey(
        Investor, on_delete=models.CASCADE, related_name='fundings')
    amount = models.DecimalField(
        max_digits=15, decimal_places=2)  # Amount funded
    transaction_id = models.CharField(
        max_length=100, unique=True, default=uuid.uuid4)
    funded_at = models.DateTimeField(auto_now_add=True)

    # Razorpay-specific fields
    razorpay_payment_id = models.CharField(
        max_length=100, null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    payment_status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('success',
                                          'Success'), ('failed', 'Failed')],
        default='pending'
    )

    def __str__(self):
        return f"{self.investor.user.email} funded {self.amount} for {self.idea_id.title}"

    def save(self, *args, **kwargs):
        """Override save method to update the total funded amount in the idea if payment is successful."""
        if not self.transaction_id:
            # Generate unique transaction ID
            self.transaction_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

        # Only update funding total if payment was successful
        if self.payment_status == 'success':
            self.idea_id.update_total_funding(self.amount)
