from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Book, Member,Transaction

# Create your views here.
# Book views
class BookListView(ListView):
    model = Book
    template_name = 'main/booklist.html'
    context_object_name = 'books'
    
class BookCreateView(CreateView):
    model = Book
    template_name = 'main/book_form.html'
    fields = ['title', 'author', 'quantity', 'rental_fee']
    success_url = reverse_lazy('books')
    
class BookUpdateView(UpdateView):
    model = Book
    template_name = 'main/book_form.html'
    fields = ['title', 'author', 'quantity', 'rental_fee']
    success_url = reverse_lazy('books')
    
class BookDeleteView(DeleteView):
    model = Book
    template_name = 'main/delete_book.html'
    success_url = reverse_lazy('books')
    
# Member views

class MemberListView(ListView):
    model = Member
    template_name = 'main/memberlist.html'
    context_object_name = 'members'
    
class MemberCreateView(CreateView):
    model = Member
    template_name = 'main/member_form.html'
    fields = ['name', 'phone_number','email', 'rental_debt']
    success_url = reverse_lazy('members')

class MemberUpdateView(UpdateView):
    model = Member
    template_name = 'main/member_form.html'
    fields = ['name', 'phone_number', 'email', 'rental_debt']
    success_url = reverse_lazy('members')
    
class MemberDeleteView(DeleteView):
    model = Member
    template_name = 'main/delete_member.html'
    success_url = reverse_lazy('members')
    
    
# Transactions
# Issue books 

class IssueBookView(CreateView):
    model = Transaction
    template_name = 'main/transaction_form.html'
    fields = ['book', 'member']
    
    def form_valid(self, form):
        transaction = form.save(commmit=False)
        if transaction.book.quantity > 0:
            transaction.book.quantity -= 1
            transaction.book.save()
            return super().form_valid(form)
        else:
            form.add_error(None, 'This book is not available')
            return self.form_invalid(form)
    def get_success_url(self):
        return reverse_lazy('books')
    
# Return books   
class ReturnBookView(CreateView):
    model = Transaction
    template_name = 'main/return_transaction_form.html'
    fields = ['book', 'member']
    
    def form_valid(self, form):
        transaction = Transaction.objects.filter(
            book = form.cleaned_data['book'],
            member = form.cleaned_data['member'],
            return_date__isnull=True  
        ).first()
        
        if transaction:
            transaction.return_date = self.request.POST.get('return_date')
            transaction.fees_charged = form.cleaned_data['book'].rental_fee
            transaction.member.rental_debt += transaction.fees_charged
            
            if transaction.member.rental_debt > 500:
                form.add_error(None, 'Member has exceeded the maximum debt limit')
                return self.form_invalid(form)
            
            transaction.save()
            transaction.book.quantity += 1
            transaction.book.save()
            return super().form_valid(form)
        
        else:
            form.add_error(None, 'This book has not been issued to any member')
            return self.form_invalid(form)
        
    def get_success_url(self):
        return reverse_lazy('books')