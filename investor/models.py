from django.db import models
from userauth.models import Investor
from student.models import IdeaSubmission


class InvestorInterest(models.Model):
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    idea = models.ForeignKey(IdeaSubmission, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.investor.full_name} interested in {self.idea.title}"


class InvestorFunding(models.Model):
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    idea = models.ForeignKey(IdeaSubmission, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.investor.full_name} funded {self.idea.title} for ${self.amount}"
