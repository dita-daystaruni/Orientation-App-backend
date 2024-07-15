# Daystar University Orientation App Backend

## Project Overview

This project is the backend for the Daystar University orientation app. It allows the orientation team to upload events, activities, FAQs, photos, short videos, titles, descriptions, dates, and venues. Freshmen can view these events, receive notifications, view FAQs, and ask questions in forums.

## Prerequisites

- Python 3.x
- Django
- Django REST framework
- django-cors-headers

## Installation

1. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run migrations:
    ```bash
    python manage.py migrate
    ```

4. Create a superuser:
    ```bash
    python manage.py createsuperuser
    ```

5. Run the development server:
    ```bash
    python manage.py runserver
    ```

## API Endpoints

- `/api/auth/`: Obtain authentication token.
- `/api/users/`: User-related endpoints
- `/api/orientations/`: Orientation-related endpoints
- `/api/events/`: Event-related endpoints
- `/api/faqs/`: FAQ-related endpoints

