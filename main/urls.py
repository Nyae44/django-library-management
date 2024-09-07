from django.urls import path
from .views import BookListView, BookCreateView, BookUpdateView, BookDeleteView, MemberListView,MemberCreateView, MemberUpdateView, MemberDeleteView, IssueBookView, ReturnBookView, WelcomePageView, DashboardView, LoginView, RegisterView,LogoutView
urlpatterns = [
    
    path('',WelcomePageView.as_view(),name='welcome'),
    path('dashboard/', DashboardView.as_view(), name='dashboard' ),
    # Books
    path('books/', BookListView.as_view(), name='books'),
    path('books/add/', BookCreateView.as_view(), name='book_create'),
    path('books/<int:pk>/edit/',BookUpdateView.as_view(), name='book_update'),
    path('books/<int:pk>/delete/',BookDeleteView.as_view(), name='book_delete'),
    
    # Members
    path('members/',MemberListView.as_view(), name='members'),
    path('members/add/', MemberCreateView.as_view(), name='member_create'),
    path('members/<int:pk>/edit/', MemberUpdateView.as_view(), name='member_update'),
    path('members/<int:pk>/delete/', MemberDeleteView.as_view(), name='member_delete'),
    
    # Transactions
    path('transaction/issue', IssueBookView.as_view(), name='issue_book'),
    path('transaction/return', ReturnBookView.as_view(), name='return_book'),
    
    #Authentication
    path('login/', LoginView.as_view(), name='login' ),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name="logout")
    
    
    
    
]
