🌾 Agriculture Crops Management System

A **full-stack Django application** for managing agriculture crops, users, and orders with **JWT authentication** and **role-based access control**.  
This system simulates a **real-world agricultural marketplace**, allowing farmers to list crops, brokers to manage listings, clients to place orders, and admins to oversee the entire system.

🛠 Technology Stack

Backend: Django 5, Django REST Framework

Frontend: Django templates with Bootstrap 5

Database: PostgreSQL (SQLite for quick local development)

Authentication: JWT (Simple JWT)

Roles: Admin, Farmer, Broker, Client

📁 Project Structure

Crops/

       config/             # Django project settings
    
       authentication/     # Auth (login, register, JWT)
    
       users/              # User CRUD, roles
    
       crops/              # Crops CRUD
    
       orders/             # Orders, status tracking
    
       dashboards/         # Role-based dashboards
    
      templates/          # HTML templates
    
      static/             # CSS, JS
    
      manage.py
    
      requirements.txt


⚙️ Setup Instructions

Create Virtual Environment

cd Crops
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate


Install Dependencies

pip install -r requirements.txt


Run Migrations

python manage.py makemigrations users crops orders
python manage.py migrate


Seed Sample Data (Optional)

python manage.py seed_data


This creates:

Admin: admin / admin123

Farmers: farmer1, farmer2 / farmer123

Broker: broker1 / broker123

Clients: client1, client2 / client123

Also seeds sample crops and orders.

Create Superuser (if not using seed)

python manage.py createsuperuser


Run Development Server

python manage.py runserver


Visit: http://127.0.0.1:8000/

🔗 API Endpoints
| Method | Endpoint                 | Description                 |
| ------ | ------------------------ | --------------------------- |
| POST   | /api/auth/register/      | Register                    |
| POST   | /api/auth/login/         | Login (returns JWT)         |
| POST   | /api/auth/token/refresh/ | Refresh JWT                 |
| GET    | /api/auth/profile/       | Current user (requires JWT) |
| POST   | /api/auth/logout/        | Logout                      |

Users (Admin only)
| Method | Endpoint         | Description |
| ------ | ---------------- | ----------- |
| GET    | /api/users/      | List users  |
| POST   | /api/users/      | Create user |
| GET    | /api/users/{id}/ | User detail |
| PUT    | /api/users/{id}/ | Update user |
| DELETE | /api/users/{id}/ | Delete user |

Crops
| Method | Endpoint         | Description                |
| ------ | ---------------- | -------------------------- |
| GET    | /api/crops/      | List crops                 |
| POST   | /api/crops/      | Create crop (Farmer/Admin) |
| GET    | /api/crops/{id}/ | Crop detail                |
| PUT    | /api/crops/{id}/ | Update crop                |
| DELETE | /api/crops/{id}/ | Delete crop                |

Orders
| Method | Endpoint                        | Description          |
| ------ | ------------------------------- | -------------------- |
| GET    | /api/orders/                    | List orders          |
| POST   | /api/orders/                    | Place order          |
| GET    | /api/orders/{id}/               | Order detail         |
| PATCH  | /api/orders/{id}/update_status/ | Update status        |
| GET    | /api/orders/{id}/history/       | Order status history |


👥 User Roles & Permissions

| Role   | Dashboard | Crops  | Orders | Users |
|--------|-----------|--------|--------|-------|
| Admin  | Full stats| All CRUD| All    | CRUD  |
| Farmer | My crops  | My CRUD| My sales| -     |
| Broker | Listings  | View   | Manage | -     |
| Client | My orders | Browse | Place  | -     |


