# Cyber security Base - Project I

Cyber Security Base 2025 course project 1

This is a demonstration of a web application with five security flaws from the OWASP 2021 top-10 list:

- A01:2021 Broken Access Control
- A03:2021 Injection
- A05:2021 Security Misconfiguration
- A07:2021 Identification and Authentication Failures
- A09:2021 Security Logging and Monitoring Failures


## Installation instructions

Clone the repository
```bash
git clone https://github.com/ttanninen/CSB2025_project1.git
cd CSB2025_project1/flawed_site
```

Set up virtual environment and build dependencies
```bash
python -m venv venv
source venv/bin/activate
pip install django
python manage.py migrate
```

Run server
```bash
python manage.py runserver
```

Use your web browser and browse to
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)



