from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView,TemplateView, FormView, View
from .models import Book, Member,Transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm, TransactionForm, ReturnBookForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from datetime import datetime

# Create your views here.

class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login') 
    
class LoginView(FormView):
    template_name = 'main/login.html'
    form_class = AuthenticationForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        # Get the username and password from the form data
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        # Authenticate the user
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            return redirect(self.success_url)
        else:
            form.add_error(None, 'Invalid username or password')
            return self.form_invalid(form)
        
@method_decorator(login_required(login_url='login'),name='dispatch')
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')
    
    
class WelcomePageView(TemplateView):
    template_name = 'main/index.html'

# Book views
@method_decorator(login_required(login_url='login'),name='dispatch')
class DashboardView(ListView):
    model = Book
    template_name = 'main/dashboard.html'
    context_object_name = 'books'
    
    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)
    
@method_decorator(login_required(login_url='login'),name='dispatch')
class BookDetailView(DetailView):
    model = Book
    template_name = 'main/view-book.html'
    context_object_name = 'book'
    
@method_decorator(login_required(login_url='login'),name='dispatch')
class BookCreateView(CreateView):
    model = Book
    template_name = 'main/create-book.html'
    fields = ['title', 'author', 'quantity', 'total_quantity','rental_fee']
    success_url = reverse_lazy('dashboard')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
        
 
@method_decorator(login_required(login_url='login'),name='dispatch')   
class BookUpdateView(UpdateView):
    model = Book
    template_name = 'main/update-book.html'
    fields = ['title', 'author', 'quantity', 'total_quantity','rental_fee']
    
    def get_queryset(self):
        return Book.objects.filter(user=self.request.user)
    
    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk':self.object.pk})
    
@method_decorator(login_required(login_url='login'),name='dispatch')
class BookDeleteView(DeleteView):
    model = Book
    template_name = 'main/delete_book.html'
    success_url = reverse_lazy('dashboard')
    
    
# Member views

@method_decorator(login_required(login_url='login'),name='dispatch')
class MemberListView(ListView):
    model = Member
    template_name = 'main/members-list.html'
    context_object_name = 'members'
    
@method_decorator(login_required(login_url='login'),name='dispatch')
class MemberCreateView(CreateView):
    model = Member
    template_name = 'main/create-member.html'
    fields = ['name', 'phone_number','email', 'rental_debt']
    success_url = reverse_lazy('members')

@method_decorator(login_required(login_url='login'),name='dispatch')
class MemberUpdateView(UpdateView):
    model = Member
    template_name = 'main/update-member.html'
    fields = ['name', 'phone_number', 'email', 'rental_debt']
    
    def get_success_url(self):
        return reverse_lazy('member_detail', kwargs={'pk':self.object.pk})
    
@method_decorator(login_required(login_url='login'),name='dispatch')
class MemberDetailView(DetailView):
    model = Member
    template_name = 'main/view-member.html'
    context_object_name = 'member'
    
@method_decorator(login_required(login_url='login'),name='dispatch')   
class MemberDeleteView(DeleteView):
    model = Member
    template_name = 'main/delete_member.html'
    success_url = reverse_lazy('members')
    
    
    
# Transactions
# Issue books 
@method_decorator(login_required(login_url='login'), name='dispatch')
class IssueBookView(CreateView):
    model = Transaction
    template_name = 'main/issue-book.html'
    form_class = TransactionForm
    # fields = ['book', 'member', 'return_date']  

    def form_valid(self, form):
        transaction = form.save(commit=False)
        transaction.issue_date = timezone.now()  # Set issue_date automatically

        # Convert issue_date to date
        if isinstance(transaction.issue_date, datetime):
            issue_date = transaction.issue_date.date()
        else:
            issue_date = transaction.issue_date

        if transaction.book.quantity > 0:
            # Reduce the quantity of the book
            transaction.book.quantity -= 1
            transaction.book.save()

            # Validate return_date and calculate rental fees
            if transaction.return_date:
                
                if isinstance(transaction.return_date, datetime):
                    return_date = transaction.return_date.date()
                else:
                    return_date = transaction.return_date
                
                rental_duration = (return_date - issue_date).days
                
                if rental_duration >= 0:
                    transaction.rental_fees_charged = rental_duration * transaction.book.rental_fee
                else:
                    # Return date is earlier than issue date
                    form.add_error('return_date', 'Return date cannot be earlier than issue date.')
                    return self.form_invalid(form)
            else:
                # Return date is missing
                form.add_error('return_date', 'Return date is required.')
                return self.form_invalid(form)
            
            transaction.save()
            return super().form_valid(form)
        else:
            # Book is not available
            form.add_error('book', 'This book is not available.')
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard')

    
# Return books   
@method_decorator(login_required(login_url='login'),name='dispatch')
class ReturnBookView(CreateView):
    model = Transaction
    template_name = 'main/return-book.html'
    form_class = ReturnBookForm
   
    
    def form_valid(self, form):
        transaction = Transaction.objects.filter(
            book = form.cleaned_data['book'],
            member = form.cleaned_data['member'],
            return_date__isnull=True,
            actual_return_date__isnull=True
        ).first()
        
        if transaction:
            # Actual return date
            transaction.actual_return_date = timezone.now().date()
            
            
            #transaction.return_date = self.request.POST.get('return_date')
            
            # rental fees 
            transaction.fees_charged = form.cleaned_data['book'].rental_fee
            
            # Check if book is returned late
            if transaction.actual_return_date > transaction.return_date:
                days_late = (transaction.actual_return_date - transaction.return_date).days
                penalty_per_day = 20
                transaction.penalty = days_late * penalty_per_day
                transaction.member.rental_debt +=transaction.penalty
                
                
            # Add rental fees to member's debt
            transaction.member.rental_debt += transaction.fees_charged
            
            if transaction.member.rental_debt > 500:
                form.add_error(None, 'Member has exceeded the maximum debt limit')
                return self.form_invalid(form)
            
            transaction.save()
            transaction.book.quantity += 1
            transaction.book.save()
            return super().form_valid(form)
        
        else:
            form.add_error(None, 'This book has not been issued to this member or has already been returned')
            return self.form_invalid(form)
        
    def get_success_url(self):
        return reverse_lazy('dashboard')
    
    

