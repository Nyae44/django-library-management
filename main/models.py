from django.db import models

# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    author = models.CharField(max_length=200, blank=True, null=True)
    quantity = models.IntegerField(default=0, blank=True, null=True)
    rental_fee = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    
    def __str__(self):
        return self.title
    
class Member(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=50, unique=True, blank=True, null=True)
    rental_debt = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    def __str__(self):
        return self.name
    
class Transaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    fees_charged = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.book.title} - {self.member.name}"
    
