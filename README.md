# David Academy Portal API

A Django REST API backend for an online nursing-exam practice system.

## Setup Instructions

### Prerequisites
- Python 3.8+
- MySQL
- Virtual environment tool (optional but recommended)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd portal_api


To get started:
1. Install dependencies: `pip install -r requirements.txt`
2. Create the MySQL database as specified in settings.py
3. Run migrations: `python manage.py migrate`
4. Create a superuser: `python manage.py createsuperuser`
5. Start the server: `python manage.py runserver`

The API can now be used by the frontend React application with proper CORS handling enabled


----------------------------------------------------------------------------------

EMAIL OTP APIS : 

curl --location 'http://127.0.0.1:8000/api/otp/request/' \
--header 'Content-Type: application/json' \
--data-raw '  {
    "identifier": "nabeelhashim.ofc@gmail.com",
    "otp_type": "email"
  }'

------

curl --location 'http://127.0.0.1:8000/api/otp/verify/' \
--header 'Content-Type: application/json' \
--data-raw '  {
    "identifier": "nabeelhashim.ofc@gmail.com",
    "otp_type": "email",
    "code": "913896"
  }'

