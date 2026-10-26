# Healthcare Backend

REST API for managing patients, doctors and patient-doctor assignments, built with
Django, Django REST Framework, PostgreSQL and JWT authentication.

## Features
- User registration and login with JWT (access and refresh tokens)
- CRUD APIs for patients (private to the user who created them)
- CRUD APIs for doctors (visible to all users, editable only by the creator)
- Assign and remove doctors for patients, with duplicate prevention
- Validation, proper HTTP status codes and environment-based configuration
- Automated tests for authentication, patients and mappings

## Tech stack
- Python 3.10+
- Django and Django REST Framework
- PostgreSQL
- djangorestframework-simplejwt
- python-decouple

## Project structure
```
healthcare_project/
├── config/      # settings, root urls, home view
├── users/       # register, login
├── patients/    # patient model, serializer, views
├── doctors/     # doctor model, serializer, permissions, views
├── mappings/    # patient-doctor mapping
├── .env.example
├── requirements.txt
└── manage.py
```

## Setup

1. **Clone the repository**
   ```
   git clone https://github.com/Surbhideep03/Healthcare_backend
   cd healthcare-backend
   ```

2. **Create and activate a virtual environment**
   ```
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS / Linux
   ```

3. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Create the PostgreSQL database** (run in `psql` as the `postgres` user)
   ```sql
   CREATE USER healthcare_user WITH PASSWORD 'your-password' CREATEDB;
   CREATE DATABASE healthcare_db OWNER healthcare_user;
   ```

5. **Configure environment variables**

   Copy `.env.example` to `.env` and fill in your values:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DB_NAME=healthcare_db
   DB_USER=healthcare_user
   DB_PASSWORD=your-password
   DB_HOST=localhost
   DB_PORT=5432
   ```
   Generate a secret key with:
   ```
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

6. **Run migrations and start the server**
   ```
   python manage.py migrate
   python manage.py runserver
   ```
   The API runs at `http://127.0.0.1:8000/`.

7. **Run the tests**
   ```
   python manage.py test
   ```

## Authentication
1. Register with `POST /api/auth/register/`.
2. Log in with `POST /api/auth/login/` to receive `access` and `refresh` tokens.
3. Send the access token on every protected request:
   ```
   Authorization: Bearer <access_token>
   ```
4. Access tokens last 60 minutes. Get a new one with
   `POST /api/auth/token/refresh/` and body `{"refresh": "<refresh_token>"}`.

## API endpoints

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| POST | /api/auth/register/ | Register a new user | No |
| POST | /api/auth/login/ | Log in and get JWT tokens | No |
| POST | /api/auth/token/refresh/ | Get a new access token | No |
| POST | /api/patients/ | Add a patient | Yes |
| GET | /api/patients/ | List your patients | Yes |
| GET | /api/patients/<id>/ | Get a patient | Yes |
| PUT | /api/patients/<id>/ | Update a patient | Yes |
| DELETE | /api/patients/<id>/ | Delete a patient | Yes |
| POST | /api/doctors/ | Add a doctor | Yes |
| GET | /api/doctors/ | List all doctors | Yes |
| GET | /api/doctors/<id>/ | Get a doctor | Yes |
| PUT | /api/doctors/<id>/ | Update a doctor (creator only) | Yes |
| DELETE | /api/doctors/<id>/ | Delete a doctor (creator only) | Yes |
| POST | /api/mappings/ | Assign a doctor to a patient | Yes |
| GET | /api/mappings/ | List mappings for your patients | Yes |
| GET | /api/mappings/<patient_id>/ | Doctors assigned to a patient | Yes |
| DELETE | /api/mappings/<id>/ | Remove a mapping | Yes |

## Sample requests

**Register**
```json
POST /api/auth/register/
{ "name": "Asha", "email": "asha@example.com", "password": "Str0ng!Pass123" }
```

**Login**
```json
POST /api/auth/login/
{ "email": "asha@example.com", "password": "Str0ng!Pass123" }
```

**Create a patient**
```json
POST /api/patients/
{ "name": "Ravi Kumar", "age": 45, "gender": "M", "address": "Noida", "medical_history": "Diabetes" }
```

**Create a doctor**
```json
POST /api/doctors/
{ "name": "Meera Singh", "email": "meera@hospital.com", "phone": "9876543210",
  "specialization": "Cardiology", "experience_years": 10 }
```

**Assign a doctor to a patient**
```json
POST /api/mappings/
{ "patient": 1, "doctor": 1 }
```

## Error handling

| Status | Meaning |
|---|---|
| 400 | Validation error (bad input, duplicate email, duplicate mapping) |
| 401 | Missing, invalid or expired token, or wrong login credentials |
| 403 | Authenticated but not allowed (editing another user's doctor) |
| 404 | Resource not found, or belongs to another user |

## Design decisions
- Email is stored as the Django `username`, so no custom user model is needed.
- Patients are private: users only see and edit patients they created. Other users' patients return 404.
- Doctors are shared: every authenticated user can view all doctors, but only the creator can edit or delete one.
- `GET /api/mappings/` returns only mappings for the current user's patients.
- A doctor can be assigned to the same patient only once (unique constraint).
- `IsAuthenticated` is the global default, so endpoints are protected unless explicitly opened (register and login).
- Secrets are loaded from environment variables and `.env` is excluded from Git.

## Author
<Your Name> - <your email or LinkedIn>
