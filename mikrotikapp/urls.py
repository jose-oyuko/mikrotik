from django.urls import path
from mikrotikapp import views
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('api/confirm_executed_command/', views.confirm_executed_commands, name='confirm_executed_command'),
    path('2/', views.packages_2, name='packages_2' ),
    path('api/sessions/active', views.ActiveSessions.as_view(), name='active-sessions'),
    path('api/pending/', csrf_exempt(views.PendingPaymentClass.as_view()), name='pending-payment'),
    path('api/payed/', views.PayedTransactions.as_view(), name='payed-transactions'),
    path('api/packages/', views.PackegesList.as_view(), name='packages-list'),
    path('api/packages/<int:pk>/', views.PackegesDetail.as_view(), name='packages-detail'),
    path('api/commands/list/', views.CommandsList.as_view(), name='commands-list'),
    path('api/commands/detail/<int:pk>/', views.CommandsDetail.as_view(), name='commands-detail'),
    path('admin/packages/', login_required(views.admin_packages), name='admin-packages'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.packages, name='packages'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/change-password/', views.change_password, name='change_password'),
    path('api/payment-status/<str:mac_address>/', csrf_exempt(views.payment_status_stream), name='payment-status-stream'),
    path('api/dashboard/', views.DashboardAPIView.as_view(), name='dashboard-api'),
    path('api/commands/', views.get_commands, name='get-commands'),
    path('api/commands/status/', views.report_status, name='report-status'),
    path('api/tickets/', views.TicketsView.as_view(), name='tickets-view'),
    path('api/tickets/<int:pk>/', views.TicketsDetail.as_view(), name='tickets-detail'),
    path('api/tickets/validate/', csrf_exempt(views.TicketValidation.as_view()), name='ticket-validation'),
    path('api/payed_date_range/', views.PayedTransactionsByDate.as_view(), name='payed-transactions-by-date'),
    path('api/actve_sessions_date_range/', views.ActiveSessionsByDateReange.as_view(), name='active-sessions-by-date'),
    path('api/mpesa_code/', views.MpesaCodeLogin.as_view(), name='mpesa-code'),
]

urlpatterns = format_suffix_patterns(urlpatterns)