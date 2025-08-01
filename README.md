# Google Drive

## Overview

**Google Drive** is a Django-based project that emulates core functionalities of the real Google Drive service. It provides a RESTful API for user authentication, file storage, file sharing, and subscription-based storage plans. The project is designed with modularity, scalability, and testability in mind, leveraging Django REST Framework, Celery for background tasks, Redis for caching, and PostgreSQL for persistent storage.

---

## Features

- **User Management**
    - User registration, login, and profile management.
    - JWT-based authentication using `djangorestframework_simplejwt`.

- **File Management**
    - Upload, retrieve, and delete files.
    - Support for chunked file uploads to handle large files efficiently.
    - File sharing with other users, including adding and removing shared users.

- **Storage Plans**
    - CRUD operations for storage plans (admin only).
    - Subscription to storage plans with Stripe integration for payments.
    - Management of user storage plans and transactions.

- **Background Tasks**
    - Asynchronous processing of file chunks using Celery.
    - Periodic cleanup of expired file upload sessions.

- **API Documentation**
    - Interactive Swagger UI available at `/__docs__/v1/`.

- **Testing**
    - Comprehensive test suite for all major endpoints and features.

---

## Technology Stack

- **Backend:** Django, Django REST Framework
- **Task Queue:** Celery with Redis as broker and result backend
- **Database:** PostgreSQL
- **Cache:** Redis
- **Authentication:** JWT (SimpleJWT)
- **Payments:** Stripe
- **Containerization:** Docker, Docker Compose
- **Web Server:** Nginx (for reverse proxy)
- **API Docs:** drf-yasg (Swagger/OpenAPI)

---

## Project Structure

- `core/` - Main Django project settings and configuration.
- `users/` - User models, authentication, and related APIs.
- `file/` - File models, upload/retrieve/delete/share APIs, and chunking utilities.
- `plan/` - Storage plan models, subscription APIs, and Stripe integration.
- `globals/` - Shared utilities, Celery tasks, and test object factories.
- `media/` - Uploaded files storage.
- `tests/` - Automated test cases for all modules.

---

## Key Endpoints

- **User APIs:** `/users/`
- **File APIs:** `/file/`
- **Plan APIs:** `/plan/`
- **API Documentation:** `/__docs__/v1/`

---

## Development & Deployment

- **Dockerized** for easy local development and deployment.
- **Celery workers** and **beat scheduler** run as separate services for background processing.
- **Nginx** serves as a reverse proxy to the Django application.

---

## Getting Started

1. Clone the repository.
2. create `.env` file inside the project and paste this code : 
    ```
    # Stripe Conf
    STRIPE_SUCCESS_URL = "http://api.localhost/checkout/success/"
    STRIPE_CANCEL_URL = "http://api.localhost/checkout/cancel/"
    STRIPE_PUBLISHABLE_KEY = "<STRIPE_PUBLISHABLE_KEY>"
    STRIPE_SECRET_KEY = "<STRIPE_SECRET_KEY>"
    # System Conf
    DATABASE_URL="postgresql://postgres:postgres@db:5432/custom_db"
    REDIS_URL="redis://redis:6379/0"
    CELERY_BROKER_URL="redis://redis:6379/1"
    CELERY_RESULT_BACKEND="redis://redis:6379/1"
    ```
2. Build and run with Docker Compose:
     ```sh
     docker-compose up --build
     ```
3. Access the API at `http://localhost/` and Swagger docs at `http://localhost/__docs__/v1/`.

---

## Notes

- This project is for educational and demonstration purposes, emulating core Google Drive features.
- Not intended for production use without further security and scalability considerations.

---