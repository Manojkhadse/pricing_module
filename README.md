#  Django Pricing Module

A configurable pricing module for managing and calculating service charges (like ride billing: Uber/Ola) based on time, distance, day, and other parameters. Built with Django and Django Admin.

---

##  Features

- Configurable pricing rules:
  - Distance Base Price (DBP)
  - Distance Additional Price (DAP)
  - Time Multiplier Factor (TMF)
  - Waiting Charges (WC)
- Day-based differential pricing
- Support for multiple configurations with active toggling
- Change logs for auditability (who changed what and when)
- Admin UI with inlines for easy configuration
- API-ready logic for price calculation

---

##  Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Manojkhadse/pricing-module.git
cd pricing-module

Step 2 Install Dependencies
    -  pip install -r requirements.txt

Step 3 Apply Migrations
    -  pip install -r requirements.txt

Step 4 Create Superuser (for Admin Access)
    -  python manage.py createsuperuser

Step 5 Run the Development Server
    - python manage.py runserver

Step 6 Access Admin Panel
    - Visit: http://127.0.0.1:8000/admin


    - Login with the superuser credentials you created.

Step 7  Hit this url in browser
    - " http://127.0.0.1:8000/api/calculate/?distance=3&time=1.5&waiting=6&day=Tue "
