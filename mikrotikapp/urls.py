from django.urls import path
from mikrotikapp  import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('pending/', views.PendingPayment.as_view(), name='pending-transactions'),
    path('payed/', views.PayedTransactions.as_view(), name='payed-transactions'),
]

urlpatterns = format_suffix_patterns(urlpatterns)