🌾 Agriculture Crops Management System (Django)

A full-stack Agriculture Crops Management System built using Python Django and Django REST Framework.  
The system is designed to manage crops, users, and orders with role-based dashboards, JWT authentication, and a clean, modern UI.

This project simulates a real-world agricultural marketplace where:
- Farmers list crops
- Brokers manage listings
- Clients place orders
- Admins oversee the entire system

---

🚀 Features

🔐 Authentication & Authorization
- User Registration & Login
- JWT-based Authentication (Simple JWT)
- Role-based Access Control (Admin, Farmer, Broker, Client)

👥 User Roles
- **Admin** – Manage users, crops, reports, approvals
- **Farmer** – Add and manage crops, stock, and pricing
- **Broker** – Manage crop listings and coordinate sales
- **Client** – Browse crops, place orders, and track order status

🌱 Crops Management (CRUD)
- Add, update, delete, and view crops
- Crop details: name, type, quantity, price, farmer, location, status

📦 Orders Management
- Place orders
- Track order status
- View order history

📊 Dashboards
- Role-based dashboards
- Statistics cards
- Tables and recent activity overview

---

🛠 Technology Stack

- **Backend:** Python, Django 5, Django REST Framework  
- **Frontend:** Django Templates, Bootstrap 5, JavaScript  
- **Database:** PostgreSQL (SQLite for quick local development)  
- **Authentication:** JWT (Simple JWT)  
- **Architecture:** RESTful APIs  

---

📁 Project Structure

Crops/
├── config/                 # Django project settings
├── authentication/         # Auth (login, register, JWT)
├── users/                  # User CRUD & roles
├── crops/                  # Crops CRUD
├── orders/                 # Orders & status tracking
├── dashboards/             # Role-based dashboards
├── templates/              # HTML templates
├── static/                 # CSS & JavaScript
├── manage.py
└── requirements.txt
⚙️ Installation & Setup

1️⃣ Clone the Repository
git clone https://github.com/amnaijaz2/Agriculture-Crops-Management-System.git
cd Crops
2️⃣ Create & Activate Virtual Environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
3️⃣ Install Dependencies
pip install -r requirements.txt
4️⃣ Environment Configuration
Create a .env file in the project root:

DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# SQLite (quick start)
DB_ENGINE=sqlite

# PostgreSQL (production)
DB_ENGINE=postgresql
DB_NAME=crops_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
5️⃣ Run Migrations
python manage.py makemigrations
python manage.py migrate
6️⃣ Create Superuser
python manage.py createsuperuser
7️⃣ Run Development Server
python manage.py runserver
Visit: http://127.0.0.1:8000/

🔑 API Authentication (JWT)

POST /api/auth/register/ – Register

POST /api/auth/login/ – Login (returns JWT)

POST /api/auth/token/refresh/ – Refresh token

GET /api/auth/profile/ – Current user (JWT required)

Example:

curl -X POST http://127.0.0.1:8000/api/auth/login/ \
-H "Content-Type: application/json" \
-d '{"username":"admin","password":"admin123"}'
📸 Screenshots (Add Your Images Here)

Login / Registration Pages

Admin / Farmer / Broker / Client Dashboards

Crops Management Pages

Orders Pages

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
