from django.urls import path
from mikrotikapp  import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('api/pending/', views.PendingPayment.as_view(), name='pending-transactions'),
    path('api/payed/', views.PayedTransactions.as_view(), name='payed-transactions'),
    path('', views.packages, name='packages'),
    path('api/packeges/', views.PackegesList.as_view(), name='package_list'),
    path('api/packeges/<int:pk>/', views.PackegesDetail.as_view(), name='package_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)