# PayLeave

A Django project for managing employee leave requests, overtime logging, and payroll calculation with role-based access for Employees and Managers.

---
## Features
- User management with two roles: **EMPLOYEE** and **MANAGER**.
- Submit and track optional leave requests (LeaveRequest) with monthly limits.
- Record and track overtime (OvertimeLog) with daily and monthly rules.
- Manage payroll runs (PayrollRun) and calculate final salaries (PayrollRecord) considering leave and overtime.
- Session-based authentication with role-based permissions.
- Fully documented REST API with **Swagger / OpenAPI**.
- Can run with **Docker / Docker Compose** for easy setup.
- Data persists across container restarts using Docker volumes.

---
## Technologies
- Python 3.12
- Django & Django REST Framework
- SQLite
- Swagger
- Docker & Docker Compose

---
## Installation
1. Clone the repository:
```bash
git clone https://github.com/Amirk22/payleave-system.git
```
```bash
cd payleave-system
```
2. Build and run the project using Docker Compose:
```bash
docker compose up --build
```
3. Access the API:
- Main API: http://localhost:8000/
- Swagger docs: http://localhost:8000/api/swagger

---
## Notes
- All salary and payroll calculations are automated based on leave and overtime logs.
- Only managers can finalize payroll runs and approve leave requests.
- Employees can submit leave requests and record overtime within the open payroll period.
- Session-based authentication is used instead of token-based, suitable for simple project setups.
