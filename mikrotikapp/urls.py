from django.urls import path
from mikrotikapp import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('api/pending/', views.PendingPayment.as_view(), name='pending-payment'),
    path('api/payed/', views.PayedTransactions.as_view(), name='payed-transactions'),
    path('api/packages/', views.PackegesList.as_view(), name='packages-list'),
    path('api/packages/<int:pk>/', views.PackegesDetail.as_view(), name='packages-detail'),
    path('admin/packages/', login_required(views.admin_packages), name='admin-packages'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.packages, name='packages'),
]

urlpatterns = format_suffix_patterns(urlpatterns)