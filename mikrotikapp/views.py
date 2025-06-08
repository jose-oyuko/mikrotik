from mikrotikapp.models import Tickets ,PendingPayment, PayedTransaction, Packages, sessions, Commands
from mikrotikapp.serializers import TicketsSerializer, PayedTransactionSerializer, PendingPaymentSerializer, PackagesSerializer, SessionsSerializers, CommandsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from loguru import logger
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .utils import save_transaction_to_json
from datetime import datetime
import json
from .services.kopokopo import Kopokopo
from .services.sessions import SessionsService
from .services.mikrotik import Mikrotik
from .services.commands import CommandsServices
from .services.tickets import TicketService
from django.views.decorators.http import require_http_methods, require_GET
from django.views.decorators.csrf import csrf_exempt
import re
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.http import StreamingHttpResponse, JsonResponse
import time as time_sleep
from .services.dashboard import Dashboard
from django.utils import timezone
from django.db.models import Sum
from django.utils.timezone import make_aware
from datetime import datetime, time
from django.utils.decorators import method_decorator
from django.utils.dateparse import parse_date


class ActiveSessionsByDateReange(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date:
            return Response({'error': 'start_date is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        start_date = parse_date(start_date)
        if not start_date:
            return Response({'error': 'Invalid start_date format'}, status=status.HTTP_400_BAD_REQUEST)
        
        if end_date:
            end_date = parse_date(end_date)
            if not end_date:
                return Response({'error': 'Invalid end_date format'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            end_date = start_date

        start_datetime = make_aware(datetime.combine(start_date, time.min))
        end_datetime = make_aware(datetime.combine(end_date, time.max))
        active_sessions = sessions.objects.filter(
            starting_time__range=(start_datetime, end_datetime)
        ).values(
            'mac_address', 'phone_number', 'starting_time', 'end_time', 'period'
        ).order_by('-starting_time')
        
        logger.info(f"Retrieved {len(active_sessions)} active sessions from {start_date} to {end_date}")
        return Response({
            'active_sessions': list(active_sessions),
            'count': len(active_sessions)
        })


class PayedTransactionsByDate(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date:
            return Response({'error': 'start_date is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        start_date = parse_date(start_date)
        if not start_date:
            return Response({'error': 'Invalid start_date format'}, status=status.HTTP_400_BAD_REQUEST)
        
        if end_date:
            end_date = parse_date(end_date)
            if not end_date:
                return Response({'error': 'Invalid end_date format'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            end_date = start_date

        start_datetime = make_aware(datetime.combine(start_date, time.min))
        end_datetime = make_aware(datetime.combine(end_date, time.max))
        transactions = PayedTransaction.objects.filter(
            origination_time__range=(start_datetime, end_datetime)
        ).values(
            'origination_time', 'amount', 'sender_phone_number', 'sender_first_name'
        ).order_by('-origination_time')
        total_amount = transactions.aggregate(total=Sum('amount'))['total'] or 0
        logger.info(f"Retrieved {len(transactions)} transactions from {start_date} to {end_date} with total amount: {total_amount}")
        return Response({
            'transactions': list(transactions),
            'total_amount': total_amount
        })
    
@method_decorator(csrf_exempt, name='dispatch')
class TicketValidation(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        mac_address = request.data.get('mac_address')
        ip_address = request.data.get('ip_address')
        ticketService = TicketService()
        ticketValid = ticketService.checkTicket(username, password)
        if not ticketValid:
            return Response({'error': 'Invalid or used ticket'}, status=status.HTTP_400_BAD_REQUEST)
        # Add session if ticket is valid
        sessionService = SessionsService()
        sessionService.add_session(
            mac_address=mac_address,
            phone_number=username,
            period=int(ticketValid),
            package_amount=0  # Assuming no package amount for tickets
        )
        logger.info(f"Ticket validated successfully for user: {username}")
        session_details = sessionService.check_session(mac_address)
        if not session_details:
            return Response({'error': 'Failed to create session'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Convert time string to minutes
        # time_str = session_details['time_remaining']
        # total_minutes = 0
        # if 'd' in time_str:
        #     days = int(time_str.split('d')[0])
        #     total_minutes += days * 24 * 60
        #     time_str = time_str.split('d')[1]
        # if 'h' in time_str:
        #     hours = int(time_str.split('h')[0])
        #     total_minutes += hours * 60
        #     time_str = time_str.split('h')[1]
        # if 'm' in time_str:
        #     minutes = int(time_str.split('m')[0])
        #     total_minutes += minutes
        
        commands = CommandsServices()
        commands.add_user(username=session_details['mac_address'], password=session_details['mac_address'], time=session_details['time_remaining'])
        commands.login(mac=mac_address, ip=ip_address, time=session_details['time_remaining'])
        return Response({'message': 'Ticket validated successfully'}, status=status.HTTP_200_OK)
        

class TicketsView(generics.ListCreateAPIView):
    queryset = Tickets.objects.all()
    serializer_class = TicketsSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        ticketPeriod = request.data.get('ticketPeriod')
        if not ticketPeriod:
            return Response({'error': 'ticketPeriod is required'}, status=status.HTTP_400_BAD_REQUEST)
        ticketService = TicketService()
        ticketData = ticketService.createTicket(ticketPeriod)
        if not ticketData:
            return Response({'error': 'Failed to create ticket'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = self.get_serializer(data=ticketData)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        logger.info(f"Ticket created successfully: {serializer.data}")
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class TicketsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tickets.objects.all()
    serializer_class = TicketsSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class CommandsList(generics.ListAPIView):
    queryset = Commands.objects.filter(executed=False)
    serializer_class = CommandsSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    

class CommandsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Commands.objects.all()
    serializer_class = CommandsSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

# authorize the user to access the commands

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_commands(request):
    logger.info("Received request to fetch unexecuted commands")
    try:
        commands = Commands.objects.filter(
            executed=False
        ).order_by('created_at')
        
        logger.info(f"Found {commands.count()} unexecuted commands")
        
        command_list = []
        for command in commands:
            command_data = {
                'id': command.id,
                'data': {
                    'type': command.comand_type,
                    'params': command.params,
                }
            }
            command_list.append(command_data)
            logger.debug(f"Added command to list: ID={command.id}, Type={command.comand_type}, Params={command.params}")
        
        logger.info(f"Successfully prepared {len(command_list)} commands for response")
        return JsonResponse({'commands': command_list})
        
    except Exception as e:
        logger.error(f"Error fetching commands: {str(e)}", exc_info=True)
        return JsonResponse({'error': 'Failed to fetch commands'}, status=500)
    
@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def report_status(request):
    try:
        data = json.loads(request.body)
        command_id = data.get('command_id')
        status_data = data.get('status')
        
        # Update the command status in the database
        command = Commands.objects.get(id=command_id)
        if status_data.get('status') == 'success':
            command.executed = True
            command.save()
            logger.info(f"Command {command_id} executed successfully")
        return JsonResponse({'message': 'Status reported successfully'}, status=200)
    except Exception as e:
        logger.error(f"Error reporting status: {str(e)}")
        return JsonResponse({'error': 'Failed to report status'}, status=500)
class PendingPaymentClass(generics.CreateAPIView):
    queryset = PendingPayment.objects.all()
    serializer_class = PendingPaymentSerializer
    

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                # initiate stk push
                payment = Kopokopo()
                payment.stk_push(amount=serializer.data["amount"], phone_number=serializer.data["phoneNumber"])
                
                logger.info(f"Created pending payment: {serializer.data}")
                return Response(
                    {
                        'message': 'Pending payment created successfully',
                        'id': serializer.data['id'],
                        'macAddress': serializer.data['macAddress']
                    },
                    status=status.HTTP_201_CREATED
                )
            logger.error(f"Validation errors: {serializer.errors}")
            return Response(
                {'error': 'Invalid data', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error creating pending payment: {str(e)}")
            return Response(
                {'error': 'Failed to create pending payment'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PayedTransactions(generics.CreateAPIView):
    queryset = PayedTransaction.objects.all()
    serializer_class = PayedTransactionSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Convert request body to string and replace 'nil' with 'null'
            if isinstance(request.body, bytes):
                body_str = request.body.decode('utf-8')
            else:
                body_str = str(request.body)
            
            body_str = body_str.replace(': nil', ': null')
            
            # Parse the modified JSON
            try:
                data = json.loads(body_str)
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error after nil replacement: {str(e)}")
                return Response(
                    {'error': 'Invalid JSON format', 'details': str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Log the incoming request data
            logger.debug(f"Received webhook data: {json.dumps(data, indent=2)}")

            # Save the complete transaction data to JSON file
            save_transaction_to_json(data)

            # Extract the required fields from the Kopokopo webhook data
            data = data.get('data', {})
            if not data:
                logger.error("No 'data' field found in webhook payload")
                return Response(
                    {'error': 'Invalid webhook payload: missing data field'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            attributes = data.get('attributes', {})
            if not attributes:
                logger.error("No 'attributes' field found in data")
                return Response(
                    {'error': 'Invalid webhook payload: missing attributes field'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            event = attributes.get('event', {})
            if not event:
                logger.error("No 'event' field found in attributes")
                return Response(
                    {'error': 'Invalid webhook payload: missing event field'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            resource = event.get('resource', {})
            if not resource:
                logger.error("No 'resource' field found in event")
                return Response(
                    {'error': 'Invalid webhook payload: missing resource field'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Log the extracted resource data
            logger.debug(f"Extracted resource data: {json.dumps(resource, indent=2)}")

            try:
                # Parse the origination time
                origination_time = resource.get('origination_time')
                if origination_time:
                    # Remove 'Z' and add timezone if present
                    if origination_time.endswith('Z'):
                        origination_time = origination_time[:-1] + '+00:00'
                    parsed_time = datetime.fromisoformat(origination_time)
                else:
                    parsed_time = datetime.now()
            except ValueError as e:
                logger.error(f"Error parsing origination_time: {str(e)}")
                parsed_time = datetime.now()

            # Prepare the data for the PayedTransaction model
            transaction_data = {
                'transaction_id': data.get('id'),
                'reference': resource.get('reference'),
                'origination_time': parsed_time,
                'sender_phone_number': resource.get('sender_phone_number'),
                'amount': resource.get('amount'),
                'till_number': resource.get('till_number'),
                'sender_first_name': resource.get('sender_first_name'),
                'sender_middle_name': resource.get('sender_middle_name'),
                'sender_last_name': resource.get('sender_last_name'),
            }

            # Process phone number to get last 9 digits before checking pending
            phone_number = transaction_data['sender_phone_number']
            if phone_number:
                digits = re.sub(r'\D', '', phone_number)
                processed_phone = digits[-9:] if len(digits) >= 9 else digits
                transaction_data['sender_phone_number'] = processed_phone

            # Log the prepared transaction data
            logger.debug(f"Prepared transaction data: {json.dumps(transaction_data, indent=2, default=str)}")

            # Create the serializer with the extracted data
            serializer = self.get_serializer(data=transaction_data)
            if not serializer.is_valid():
                logger.error(f"Serializer validation errors: {serializer.errors}")
                return Response(
                    {'error': 'Invalid transaction data', 'details': serializer.errors},
                    status=status.HTTP_400_BAD_REQUEST
                )

            self.perform_create(serializer)
            # pop pending, login the user
            self.check_pending(processed_phone, transaction_data['amount'])
            logger.info(f"Payment transaction processed successfully: {transaction_data['reference']}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(f"Error processing payment transaction: {str(e)}")
            return Response(
                {'error': 'Failed to process payment transaction', 'details': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
    def check_pending(self, phone_number, amount):
        try:
            # Check if there's a pending payment for this phone number and amount
            amount = int(float(amount))
            pending_payment = PendingPayment.objects.filter(
                phoneNumber=phone_number,
                amount=amount,
                payed=False
            ).first()

            if not pending_payment:
                logger.info(f"No pending payment found for phone: {phone_number}, amount: {amount}")
                return False

            # Update payment status to paid
            pending_payment.payed = True
            pending_payment.save()
            logger.info(f"Updated payment status for phone: {phone_number}")

            # Get package details
            package = Packages.objects.filter(price=amount).first()
            if not package:
                logger.error(f"No package found for amount: {amount}")
                return False

            # Add session for the user
            session_service = SessionsService()
            session_service.add_session(
                mac_address=pending_payment.macAddress,
                phone_number=phone_number,
                period=package.period_in_minutes,
                package_amount=amount
            )
            logger.info(f"Added session for phone: {phone_number}")

            # Check and return session details
            session_details = session_service.check_session(pending_payment.macAddress)
            if session_details:
                logger.info(f"Session details retrieved for phone: {phone_number}")
                # mikrotik = Mikrotik()
                # mikrotik.add_user(session_details['mac_address'], session_details['mac_address'], session_details['time_remaining'])
                # try:
                #     mikrotik.login_user(session_details['mac_address'], pending_payment.ipAddress)
                # except Mikrotik.ReAddUserError:
                #     mikrotik.add_user(session_details['mac_address'], session_details['mac_address'], session_details['time_remaining'])
                #     mikrotik.login_user(session_details['mac_address'], pending_payment.ipAddress)
                commands = CommandsServices()
                commands.add_user(username=session_details['mac_address'], password=session_details['mac_address'], time=session_details['time_remaining'])
                commands.login(mac=session_details['mac_address'], ip=pending_payment.ipAddress, time=session_details['time_remaining'])
                logger.info(f"User logged in successfully for phone: {phone_number}")
                return 

            logger.error(f"Failed to retrieve session details for phone: {phone_number}")
            return False

        except Exception as e:
            logger.error(f"Error in check_pending: {str(e)}")
            return False

class PackegesList(generics.ListCreateAPIView):
    queryset = Packages.objects.all()
    serializer_class = PackagesSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

class PackegesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Packages.objects.all()
    serializer_class = PackagesSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

class ActiveSessions(generics.ListAPIView):
    queryset = sessions.objects.filter(end_time__gt=timezone.now())
    serializer_class = SessionsSerializers
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


def login_view(request):
    if request.user.is_authenticated:
        return redirect('admin-packages')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', 'admin-packages')
            return redirect(next_url)
        else:
            return render(request, 'login.html', {'form': {'errors': True}})
    return render(request, 'login.html')

@login_required(login_url='/login/')
def admin_packages(request):
    packages = Packages.objects.all()
    return render(request, 'admin.html', {'packages': packages})

def logout_view(request):
    logout(request)
    return redirect('login')

@csrf_exempt
@require_http_methods(["POST"])
def packages(request):
    # get form data
    user_data = {
    "mac" : request.POST.get("mac"),
    "ip" : request.POST.get("ip"),
    "username" : request.POST.get("username"),
    "link_login" : request.POST.get("link-login"),
    "link_login_only" : request.POST.get("link-login-only"),
    "link_orig" : request.POST.get("link-orig"),
    }
    # check if session exists
    print(f"the mac address is {user_data['mac']}")
    session_service = SessionsService()
    session = session_service.check_session(mac_address=user_data['mac'])
    if session:
        # mikrotik = Mikrotik()
        # mikrotik.add_user(username=session['mac_address'], password=session['mac_address'], time=session['time_remaining'])
        # mikrotik.login_user(mac=session['mac_address'], ip=user_data['ip'])

        command = CommandsServices()
        command.add_user(username=session['mac_address'], password=session['mac_address'], time=session['time_remaining'])
        command.login(mac=user_data['mac'], ip=user_data['ip'], time=session['time_remaining'])
    
    packages = Packages.objects.all()

    context = {
        'packages': packages,
        'user_data': user_data
    }
    return render(request, 'packages.html', context)

@login_required(login_url='/login/')
def admin_dashboard(request):
    try:
        dashboard_service = Dashboard()
        
        # Get dashboard data
        transactions_data = dashboard_service.payed_today()
        pending_payments_data = dashboard_service.pending_payment()
        
        # Get active sessions
        active_sessions = sessions.objects.filter(end_time__gt=timezone.now())
        
        # Get all packages
        packages = Packages.objects.all()
        
        context = {
            'transactions': transactions_data['transactions'],
            'pending_payments': pending_payments_data['pending_payments'],
            'active_sessions': active_sessions,
            'packages': packages,
            'total_paid': transactions_data['total_amount'],
            'total_pending': pending_payments_data['total_amount'],
            'active_tab': 'dashboard'
        }
        return render(request, 'admin.html', context)
    except Exception as e:
        logger.error(f"Error in admin_dashboard: {str(e)}")
        messages.error(request, "Failed to load dashboard data")
        return render(request, 'admin.html', {
            'transactions': [],
            'pending_payments': [],
            'active_sessions': [],
            'packages': Packages.objects.all(),
            'total_paid': 0,
            'total_pending': 0,
            'active_tab': 'dashboard'
        })

@login_required(login_url='/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('admin_dashboard')
        else:
            # Combine all errors into a single message
            error_message = ' '.join([f'{field}: {error}' for field, errors in form.errors.items() for error in errors])
            messages.error(request, error_message)
    return redirect('admin_dashboard')

@csrf_exempt
@require_GET
def payment_status_stream(request, mac_address):
    def event_stream():
        while True:
            session_service = SessionsService()
            session = session_service.check_session(mac_address)
            if session:
                yield f"data: {json.dumps({'status': 'success', 'link_orig': session.get('link_orig', 'https://google.com')})}\n\n"
                break
            yield "data: {}\n\n"
            time_sleep.sleep(2)  # Check every 2 seconds
    
    response = StreamingHttpResponse(event_stream(), content_type='text/event-stream')
    response['Cache-Control'] = 'no-cache'
    response['X-Accel-Buffering'] = 'no'
    return response

class DashboardAPIView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            dashboard_service = Dashboard()
            
            # Get today's transactions and pending payments
            transactions_data = dashboard_service.payed_today()
            pending_payments_data = dashboard_service.pending_payment()
            
            return Response({
                'transactions': transactions_data['transactions'],
                'pending_payments': pending_payments_data['pending_payments']
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error fetching dashboard data: {str(e)}")
            return Response(
                {'error': 'Failed to fetch dashboard data'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )