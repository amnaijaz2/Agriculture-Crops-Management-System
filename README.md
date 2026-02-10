🌾 Agriculture Crops Management System (Django)

A full-stack Django application** for managing agriculture crops, users, and orders with JWT authentication and **role-based access control**.  
This system simulates a **real-world agricultural marketplace**, allowing farmers to list crops, brokers to manage listings, clients to place orders, and admins to oversee the entire system.

---

## 🛠 Technology Stack

- **Backend:** Django 5, Django REST Framework  
- **Frontend:** Django Templates with Bootstrap 5  
- **Database:** PostgreSQL (SQLite for quick local development)  
- **Authentication:** JWT (Simple JWT)  
- **Roles:** Admin, Farmer, Broker, Client  

---

## 📁 Project Structure

Crops/
├── config/ # Django project settings
├── authentication/ # Auth (login, register, JWT)
├── users/ # User CRUD & roles
├── crops/ # Crops CRUD
├── orders/ # Orders & status tracking
├── dashboards/ # Role-based dashboards
├── templates/ # HTML templates
├── static/ # CSS, JS
├── manage.py
└── requirements.txt


---

## ⚙️ Setup Instructions

### 1️⃣ Create Virtual Environment
```bash
cd Crops
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Environment Configuration
Create a .env file in the project root (copy from .env.example):

DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# SQLite (quick local setup)
DB_ENGINE=sqlite

# PostgreSQL (production)
DB_ENGINE=postgresql
DB_NAME=crops_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
4️⃣ Run Migrations
python manage.py makemigrations users crops orders
python manage.py migrate
5️⃣ Seed Sample Data (Optional)
python manage.py seed_data
Creates default users and sample crops/orders:

Admin: admin / admin123

Farmers: farmer1, farmer2 / farmer123

Broker: broker1 / broker123

Clients: client1, client2 / client123

6️⃣ Create Superuser (if not using seed)
python manage.py createsuperuser
7️⃣ Run Development Server
python manage.py runserver
Visit: http://127.0.0.1:8000/

🔑 API Endpoints
Authentication
POST /api/auth/register/ – Register

POST /api/auth/login/ – Login (returns JWT)

POST /api/auth/token/refresh/ – Refresh JWT

GET /api/auth/profile/ – Current user (requires JWT)

POST /api/auth/logout/ – Logout

Users (Admin only)
GET /api/users/ – List users

POST /api/users/ – Create user

GET /api/users/{id}/ – User detail

PUT /api/users/{id}/ – Update user

DELETE /api/users/{id}/ – Delete user

Crops
GET /api/crops/ – List crops

POST /api/crops/ – Create crop (Farmer/Admin)

GET /api/crops/{id}/ – Crop detail

PUT /api/crops/{id}/ – Update crop

DELETE /api/crops/{id}/ – Delete crop

Orders
GET /api/orders/ – List orders

POST /api/orders/ – Place order

GET /api/orders/{id}/ – Order detail

PATCH /api/orders/{id}/update_status/ – Update status

GET /api/orders/{id}/history/ – Order status history

Example: Using API with JWT
# Login
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Use returned access token
curl http://127.0.0.1:8000/api/crops/ \
  -H "Authorization: Bearer <access_token>"
👥 User Roles & Permissions
Role	Dashboard	Crops	Orders	Users
Admin	Full stats	All CRUD	All	CRUD
Farmer	My crops	My CRUD	My sales	-
Broker	Listings	View	Manage	-
Client	My orders	Browse	Place	-

🎯 Purpose of Project
This project demonstrates:

Django backend development

REST API design

Role-based authorization & JWT authentication

Clean UI/UX with responsive dashboards

Real-world agriculture marketplace workflow

Scalable & modular project architecture

📸 Screenshots (Add your images here later)

Login / Registration

Admin / Farmer / Broker / Client Dashboards

Crops Management Pages

Orders Pages

Example Markdown to add images:
![Admin Dashboard](screenshots/admin_dashboard.png)

Add images using markdown syntax:
![Alt text](screenshots/login.png)
## User Roles & Permissions

| Role   | Dashboard | Crops  | Orders | Users |
|--------|-----------|--------|--------|-------|
| Admin  | Full stats| All CRUD| All    | CRUD  |
| Farmer | My crops  | My CRUD| My sales| -     |
| Broker | Listings  | View   | Manage | -     |
| Client | My orders | Browse | Place  | -     |

## License

MIT
