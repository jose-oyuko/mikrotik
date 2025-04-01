# Mikrotik Payment Integration

This Django application integrates Mikrotik hotspot with mobile money payments through Kopokopo API. It allows users to pay for internet access using M-Pesa and automatically logs them into the Mikrotik hotspot.

## Features

- Mobile money payment integration with Kopokopo API
- Automatic Mikrotik hotspot user management
- IP and MAC address binding
- Transaction tracking and management
- Rate limiting and security features

## Prerequisites

- Python 3.8 or higher
- Django 4.2 or higher
- Mikrotik Router with hotspot enabled
- Kopokopo API credentials

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd mikrotik
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the following variables:

```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Kopokopo API credentials
KOPOKOPO_BASE_URL=https://api.kopokopo.com
KOPOKOPO_CLIENT_ID=your-client-id
KOPOKOPO_CLIENT_SECRET=your-client-secret
KOPOKOPO_CALLBACK_URL=https://your-domain.com/api/payed/

# Mikrotik settings
MIKROTIK_HOST=your-router-ip
MIKROTIK_USERNAME=admin
MIKROTIK_PASSWORD=your-password
MIKROTIK_USER_PROFILE=default
MIKROTIK_UPTIME_LIMIT=1d
```

5. Create the logs directory:

```bash
mkdir logs
```

6. Run migrations:

```bash
python manage.py migrate
```

7. Create a superuser:

```bash
python manage.py createsuperuser
```

## Running the Application

1. Development server:

```bash
python manage.py runserver
```

2. Production server:

```bash
gunicorn mikrotik.wsgi:application
```

## API Endpoints

### Pending Payments

- `GET /api/pending/` - List all pending payments
- `POST /api/pending/` - Create a new payment request

Request body:

```json
{
  "phoneNumber": "+254712345678",
  "macAddress": "00:11:22:33:44:55",
  "ipAddress": "192.168.1.100",
  "amount": "100.00"
}
```

### Completed Payments

- `POST /api/payed/` - Handle payment callback from Kopokopo

Request body:

```json
{
  "phoneNumber": "+254712345678",
  "amountPayed": "100.00",
  "package": "daily",
  "transaction_id": "unique-transaction-id"
}
```

## Security Considerations

1. Always use HTTPS in production
2. Keep your secret key and API credentials secure
3. Set appropriate rate limits
4. Regularly update dependencies
5. Monitor logs for suspicious activity

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
