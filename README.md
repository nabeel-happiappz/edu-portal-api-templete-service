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

<<<<<<< Updated upstream
=======

----------------------------------------------------------------------------------
David Academy Portal API - APIs
---------------------------------------------------------------------------------
# Portal API

## HTTPS Configuration Guide

### Setup for Development

1. Install required packages:
   ```
   pip install -r requirements.txt
   ```

2. Generate a self-signed certificate for local development:
   ```
   openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout dev.key -out dev.crt
   ```

3. Run the development server with SSL:
   ```
   python manage.py runserver_plus --cert-file dev.crt --key-file dev.key
   ```
   Note: You'll need to install django-extensions for this feature.

### Setup for Production

1. Set the following environment variables:
   ```
   DJANGO_DEBUG=False
   DJANGO_SECRET_KEY=your_secret_key_here
   ```

2. Use a proper SSL certificate from a trusted provider like Let's Encrypt.

3. Configure your web server (Nginx/Apache) to handle SSL termination.

4. Example Nginx configuration for SSL:
   ```
   server {
       listen 443 ssl;
       server_name davidacademy.in www.davidacademy.in;

       ssl_certificate /path/to/cert.pem;
       ssl_certificate_key /path/to/key.pem;

       # Strong SSL settings
       ssl_protocols TLSv1.2 TLSv1.3;
       ssl_prefer_server_ciphers on;
       ssl_ciphers 'ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';

       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto https;
       }
   }

   # Redirect HTTP to HTTPS
   server {
       listen 80;
       server_name davidacademy.in www.davidacademy.in;
       return 301 https://$host$request_uri;
   }
   ```

5. Make sure your firewall allows traffic on ports 80 and 443.

### Testing HTTPS

After setup, verify your HTTPS configuration using:
- Browser access (check for padlock icon)
- SSL testing tools: [SSL Labs](https://www.ssllabs.com/ssltest/)
### Question APIs

curl --location 'http://127.0.0.1:8000/api/questions/' \
--header 'Content-Type: application/json' \
--data '{
    "question_type": 1,
    "content": "What is the capital of France?",
    "options": {
        "A": "London",
        "B": "Paris",
        "C": "Berlin",
        "D": "Madrid"
    },
    "correct_answer": {
        "answer": "B"
    },
    "explanation": "Paris is the capital and largest city of France",
    "duration": 2,
    "department": "Geography",
    "courses": ["World Geography", "European Studies"],
    "roles": ["student", "user"]
}'

-------------------------------------------------------------------------------------------

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

>>>>>>> Stashed changes
