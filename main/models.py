from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200, blank=True, null=True)
    author = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    total_quantity = models.IntegerField(default=0, null=True, blank=True)
    rental_fee = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    
    def __str__(self):
        return self.title
    
class Member(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=50, unique=True, blank=True, null=True)
    rental_debt = models.DecimalField(max_digits=6, decimal_places=2, default=0, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
      
    def add_to_debt(self, amount):
        """Add a specified amount to the member's debt."""
        self.rental_debt += amount
        self.save()
    
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(blank=True, null=True)
    actual_return_date = models.DateField(blank=True, null=True)
    fees_charged = models.DecimalField(max_digits=6, decimal_places=2, default=0,null=True)
    penalty = models.DecimalField(max_digits=5,decimal_places=2,default=0.0, null=True)
    
    def __str__(self):
        return f"{self.book.title} issued to {self.member.name}"
    
