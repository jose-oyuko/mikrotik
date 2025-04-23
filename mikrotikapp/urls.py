from django.urls import path
from mikrotikapp import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('api/sessions/active', views.ActiveSessions.as_view(), name='active-sessions'),
    path('api/pending/', views.PendingPaymentClass.as_view(), name='pending-payment'),
    path('api/payed/', views.PayedTransactions.as_view(), name='payed-transactions'),
    path('api/packages/', views.PackegesList.as_view(), name='packages-list'),
    path('api/packages/<int:pk>/', views.PackegesDetail.as_view(), name='packages-detail'),
    path('admin/packages/', login_required(views.admin_packages), name='admin-packages'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.packages, name='packages'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/change-password/', views.change_password, name='change_password'),
    path('api/payment-status/<str:mac_address>/', views.payment_status_stream, name='payment-status-stream'),
    path('api/dashboard/', views.DashboardAPIView.as_view(), name='dashboard-api'),
]

urlpatterns = format_suffix_patterns(urlpatterns)