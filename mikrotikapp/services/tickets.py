import random
import string
from mikrotikapp.models import Tickets
from mikrotikapp.services.sessions import SessionsService
from mikrotikapp.serializers import TicketsSerializer
from loguru import logger

class TicketService:
    def generate_random_word(self, length=5):
        return ''.join(random.choices(string.ascii_lowercase, string.digits, k=length))

    def createTicket(self, ticketPeriod):
        """
        Create a new ticket in the database.
        """
        ticketUsername = self.generate_random_word()
        ticketPassword = self.generate_random_word()
        while ticketPassword == ticketUsername:
            ticketPassword = self.generate_random_word()
        ticketPeriod = ticketPeriod
        ticketData = {
            "ticketUsername": ticketUsername,
            "ticketPassword": ticketPassword,
            "ticketPeriod": ticketPeriod
        }
        logger.info(f"Creating ticket with username: {ticketUsername} and password: {ticketPassword}")
        
        return ticketData
            
       

    def checkTicket(self, ticketUsername, ticketPassword):
        """
        Check if a ticket is valid and not used.
        """
        try:
            ticket = Tickets.objects.get(ticketUsername=ticketUsername, ticketPassword=ticketPassword)
            if ticket.used:
                return False
            else:
                # add session
                # sessionService = SessionsService()
                # sessionService.add_session(mac_address, phone_number, period, package_amount)
                ticketPeriod = ticket.ticketPeriod
                # Mark the ticket as used
                ticket.used = True
                ticket.save()
                return ticketPeriod
        except Tickets.DoesNotExist:
            return False