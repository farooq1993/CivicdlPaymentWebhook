# CivicdlPaymentWebhook

# Django Payment Webhook Receiver

This Django application provides a **Webhook Receiver** for payment events (e.g., Razorpay or PayPal).  
It supports **single or batch payloads**, validates a **simulated HMAC signature**, and stores payment events in a PostgreSQL database with **idempotency** checks.

---

## Table of Contents

- [Features](#features)  
- [Requirements](#requirements)  
- [Installation](#installation)  
- [Configuration](#configuration)  
- [Database Model](#database-model)  
- [Webhook Endpoint](#webhook-endpoint)  
- [Usage](#usage)  
- [Testing with cURL](#testing-with-curl)  
- [Example Payloads](#example-payloads)  
- [License](#license)

---

## Features

- Accepts JSON webhook payloads in Razorpay or PayPal format.  
- Validates **simulated HMAC SHA256 signature** using a predefined secret (`test_secret`).  
- Rejects requests with:
  - Missing or incorrect signature (403 Forbidden)  
  - Invalid JSON (400 Bad Request)  
- Parses and stores:
  - `event_type`  
  - `event_id`  
  - `payment_id`  
  - `amount` and `currency`  
- Supports **idempotency**: prevents duplicate processing of the same `event_id`.  
- Handles **single object** or **list payloads**.  

---

## Requirements

- Python 3.11+  
- Django 4+  
- Django REST Framework  
- PostgreSQL (or any Django-supported database)  

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/farooq1993/payment-webhook.git
cd payment-webhook


2. Create a virtual environment
python -m venv env
source env/bin/activate  # Linux/macOS
env\Scripts\activate     # Windows

3. Install dependencies
pip install -r requirements.txt

4. Apply migrations:
python manage.py makemigrations
python manage.py migrate

5. Create .env file in root directory
  DATABASE_NAME="civicpayment"
  DATABASE_USER="postgres"
  DATABASE_PASSWORD="123456"
  DATABASE_HOST="localhost"
  DATABASE_PORT="5432" 
  SHARED_SECRET="test_secret"
