from django.contrib import admin
from .models import Book, Member, Transaction


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'quantity', 'rental_fee']
    
@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['name','phone_number', 'email', 'rental_debt', 'creation_date']
    
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['book', 'member', 'issue_date', 'return_date', 'fees_charged']