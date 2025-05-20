import random
import string
from mikrotikapp.models import Tickets
from mikrotikapp.services.sessions import SessionsService
from mikrotikapp.serializers import TicketsSerializer

class TicketService:
    def generate_random_word(self, length=4):
        return ''.join(random.choices(string.ascii_lowercase, k=length))

    def createTicket(self, ticketPeriod):
        """
        Create a new ticket in the database.
        """
        ticketUsername = self.generate_random_word()
        ticketPassword = self.generate_random_word()
        ticketPeriod = ticketPeriod
        ticketData = {
            "ticketUsername": ticketUsername,
            "ticketPassword": ticketPassword,
            "ticketPeriod": ticketPeriod
        }
        
        return ticketData
            
       

    def checkTicket(self, ticketUsername, ticketPassword, mac_address, phone_number, period, package_amount):
        """
        Check if a ticket is valid and not used.
        """
        try:
            ticket = Tickets.objects.get(ticketUsername=ticketUsername, ticketPassword=ticketPassword)
            if ticket.used:
                return False
            else:
                # add session
                sessionService = SessionsService()
                sessionService.add_session(mac_address, phone_number, period, package_amount)
                return True
        except Tickets.DoesNotExist:
            return False