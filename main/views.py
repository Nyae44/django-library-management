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
from django.db.models import Q
from django.contrib import messages

# Create your views here.

class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'main/register.html'
    success_url = reverse_lazy('login') 
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Account created successfully!")
        return response
    def form_invalid(self, form):
        messages.error(self.request, "There was a problem in creating your account! Please try again")
        return super().form_invalid(form)
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
            messages.success(self.request, f"Welcome back, {username}")
            return redirect(self.success_url)
        else:
            form.add_error(None, 'Invalid username or password')
            messages.error(self.request, "Invalid username or password. Please try again!")
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
        query = self.request.GET.get('q')
        if query:
            return Book.objects.filter(
                Q(title__icontains=query) | Q(author__icontains=query), 
                user=self.request.user
            )
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
        messages.success(self.request, "Book added successfully!")
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
    
    def form_valid(self, form):
        messages.success(self.request, "Book updated successfully!")
        return super().form_valid(form)
    
        
@method_decorator(login_required(login_url='login'),name='dispatch')
class BookDeleteView(DeleteView):
    model = Book
    template_name = 'main/delete_book.html'
    success_url = reverse_lazy('dashboard')
    
    def delete(self, request, *args, **kwargs):
        book = self.get_object()
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, f'{book.title} was deleted successfully!')
        return response
    
    
# Member views
@method_decorator(login_required(login_url='login'), name='dispatch')
class MemberListView(ListView):
    model = Member
    template_name = 'main/members-list.html'
    context_object_name = 'members'
    
    def get_queryset(self):
        # Get the search query from the GET request
        query = self.request.GET.get('q', '')
        # Filter members based on the query
        if query:
            return Member.objects.filter(
                Q(name__icontains=query) | Q(phone_number__icontains=query)
            )
        return Member.objects.all()

@method_decorator(login_required(login_url='login'),name='dispatch')
class MemberCreateView(CreateView):
    model = Member
    template_name = 'main/create-member.html'
    fields = ['name', 'phone_number','email', 'rental_debt']
    success_url = reverse_lazy('members')
    
    def form_valid(self, form):
        messages.success(self.request, f"Memmber {form.instance.name} created successfully!")
        return super().form_valid(form)

@method_decorator(login_required(login_url='login'),name='dispatch')
class MemberUpdateView(UpdateView):
    model = Member
    template_name = 'main/update-member.html'
    fields = ['name', 'phone_number', 'email', 'rental_debt']
    
    def get_success_url(self):
        return reverse_lazy('member_detail', kwargs={'pk':self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, f"Member {form.instance.name} updated successfully")
        return super().form_valid(form)
    
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
    
    def member(self, request, *args, **kwargs):
        member = self.get_object()
        response = super().delete(request, *args, **kwargs)
        messages.success(self.request, f"Member {member.name} deleted successfully!")
    
# Transactions
# Issue books 
@method_decorator(login_required(login_url='login'), name='dispatch')
class IssueBookView(CreateView):
    model = Transaction
    template_name = 'main/issue-book.html'
    form_class = TransactionForm

    def form_valid(self, form):
        transaction = form.save(commit=False)
        transaction.issue_date = timezone.now()  # Set issue_date automatically

        # Convert issue_date to date
        if isinstance(transaction.issue_date, datetime):
            issue_date = transaction.issue_date.date()
        else:
            issue_date = transaction.issue_date

        # Check if the member has exceeded or reached the debt limit
        debt_limit = 500  # Set the debt limit here
        if transaction.member.rental_debt >= debt_limit:
            form.add_error(None, 'This member has reached or exceeded the rental debt limit and cannot be issued a new book.')
            return self.form_invalid(form)

        # Check if the book is available
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
                    
                    # Add the rental fee to the member's rental debt
                    transaction.member.rental_debt += transaction.rental_fees_charged
                    transaction.member.save()  # Save the updated rental debt
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
    success_url = reverse_lazy('dashboard')
   
    def form_valid(self, form):
        transaction = Transaction.objects.filter(
            book=form.cleaned_data['book'],
            member=form.cleaned_data['member'],
            actual_return_date__isnull=True
        ).first()

        if transaction:
            transaction.actual_return_date = timezone.now().date()
            transaction.fees_charged = transaction.book.rental_fee
            
            # Add fees and penalties to the member's debt
            transaction.member.add_to_debt(transaction.fees_charged)
            
            if transaction.actual_return_date > transaction.return_date:
                days_late = (transaction.actual_return_date - transaction.return_date).days
                penalty_per_day = 20
                transaction.penalty = days_late * penalty_per_day
                transaction.member.add_to_debt(transaction.penalty)
            
            # Check if debt exceeds limit
            if transaction.member.rental_debt > 500:
                form.add_error(None, 'Member has exceeded the maximum debt limit.')
                return self.form_invalid(form)

            transaction.save()
            transaction.book.quantity += 1
            transaction.book.save()
            return super().form_valid(form)
        else:
            form.add_error(None, 'This book has not been issued to this member or has already been returned.')
            return self.form_invalid(form)

        
    

