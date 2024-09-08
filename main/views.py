from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView, FormView, View
from .models import Book, Member,Transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils import timezone
from datetime import timedelta

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
    
@method_decorator(login_required(login_url='login'),name='dispatch')
class BookListView(ListView):
    model = Book
    template_name = 'main/view-book.html'
    context_object_name = 'books'
    
@method_decorator(login_required(login_url='login'),name='dispatch')
class BookCreateView(CreateView):
    model = Book
    template_name = 'main/create-book.html'
    fields = ['title', 'author', 'quantity', 'rental_fee']
    success_url = reverse_lazy('books')
 
@method_decorator(login_required(login_url='login'),name='dispatch')   
class BookUpdateView(UpdateView):
    model = Book
    template_name = 'main/update-book.html'
    fields = ['title', 'author', 'quantity', 'rental_fee']
    success_url = reverse_lazy('books')
    
@method_decorator(login_required(login_url='login'),name='dispatch')
class BookDeleteView(DeleteView):
    model = Book
    template_name = 'main/delete_book.html'
    success_url = reverse_lazy('books')
    
    
# Member views

@method_decorator(login_required(login_url='login'),name='dispatch')
class MemberListView(ListView):
    model = Member
    template_name = 'main/view-member.html'
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
    success_url = reverse_lazy('members')
    
@method_decorator(login_required(login_url='login'),name='dispatch')   
class MemberDeleteView(DeleteView):
    model = Member
    template_name = 'main/delete_member.html'
    success_url = reverse_lazy('members')
    
    
# Transactions
# Issue books 
@method_decorator(login_required(login_url='login'),name='dispatch')
class IssueBookView(CreateView):
    model = Transaction
    template_name = 'main/issue-book.html'
    fields = ['book', 'member']
    
    def form_valid(self, form):
        transaction = form.save(commit=False)
        if transaction.book.quantity > 0:
            transaction.book.quantity -= 1
            transaction.book.save()
            
            # Calculate rental_fees based on rental duration
            rental_duration = (transaction.return_date - transaction.issue_date).days
            transaction.rental_fees_charged = rental_duration * transaction.book.rental_fee # daily rental fee
            transaction.save()           
            return super().form_valid(form)
        else:
            form.add_error(None, 'This book is not available')
            return self.form_invalid(form)
    def get_success_url(self):
        return reverse_lazy('books')
    
# Return books   
@method_decorator(login_required(login_url='login'),name='dispatch')
class ReturnBookView(CreateView):
    model = Transaction
    template_name = 'main/return-book.html'
    fields = ['book', 'member']
    
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
        return reverse_lazy('books')
    
    

