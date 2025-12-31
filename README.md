# Workflow_Automation_Engine_-WAE-
A role-based workflow management system built with Python and Django, enabling Employees, Managers, and HR to submit, review, and approve requests through configurable workflow steps and transitions, with authentication, authorization, and REST API support.

# Workflow Automation Engine (WAE)

A role-based workflow automation system built using Django.

## Features
- Role-based approvals (Employee, Manager, HR)
- Configurable workflows and transitions
- Secure authentication & authorization
- REST API endpoints for workflow actions
- Clean dashboard for workflow actions

## Tech Stack
- Python
- Django
- Django REST Framework
- SQLite (Development)
- HTML & CSS

## Setup Instructions
```bash
git clone <repo-url>
cd Workflow_Automation_Engine_(WAE)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
