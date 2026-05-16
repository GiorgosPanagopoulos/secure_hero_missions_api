<div align="center">

# 🦸 Secure Hero Missions API

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)

A production-ready REST API for managing heroes and their missions, secured with JWT authentication and role-based access control.

</div>

---

## Features

| Feature | Description |
|---|---|
| 🔐 JWT Authentication | Secure token-based auth with bcrypt password hashing |
| 👑 Role-Based Access | Admin vs regular user permission tiers |
| 🦸 Hero Management | Full CRUD with partial updates |
| 🎯 Mission Tracking | Assign missions to heroes, track completion |
| 🔗 Business Rules | Enforced constraints (e.g. no delete with active missions) |
| 📖 Auto Docs | Interactive Swagger UI at `/docs` |

---

## Architecture

```mermaid
graph LR
    Client["🖥️ Client"] --> FastAPI["⚡ FastAPI"]
    FastAPI --> Auth["🔑 Auth Router"]
    FastAPI --> Heroes["🦸 Heroes Router"]
    FastAPI --> Missions["🎯 Missions Router"]
    Auth --> SQLModel["🗄️ SQLModel ORM"]
    Heroes --> SQLModel
    Missions --> SQLModel
    SQLModel --> SQLite["💾 SQLite"]
```

---

## Quick Start

```bash
git clone https://github.com/GiorgosPanagopoulos/secure-hero-missions-api.git
cd secure-hero-missions-api/hero_api
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API docs available at: `http://localhost:8000/docs`

---

## API Endpoints

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `POST` | `/auth/register` | Public | Register a new user |
| `POST` | `/auth/login` | Public | Login and receive JWT token |
| `GET` | `/auth/me` | Authenticated | Get current user info |
| `POST` | `/heroes/` | Authenticated | Create a new hero |
| `GET` | `/heroes/` | Public | List all heroes |
| `GET` | `/heroes/{id}` | Public | Get hero by ID |
| `PATCH` | `/heroes/{id}` | Authenticated | Partial update hero |
| `DELETE` | `/heroes/{id}` | Admin only | Delete hero (no active missions) |
| `POST` | `/missions/` | Authenticated | Create a mission for a hero |
| `GET` | `/missions/` | Public | List all missions |
| `GET` | `/missions/{id}` | Public | Get mission by ID |
| `PATCH` | `/missions/{id}` | Authenticated | Partial update mission |
| `DELETE` | `/missions/{id}` | Admin only | Delete mission |

---

## Testing

```bash
pytest tests/ -v
```

All 7 tests cover registration, login, token auth, role enforcement, and business rules.

---

## 📸 Screenshots

### Swagger UI Overview

![Swagger Overview](screenshots/swagger-overview.png)

### Missions Endpoints

![Swagger Missions](screenshots/swagger-missions.png)

### Register — 201 Created

![Register 201](screenshots/register-201.png)

### Tests Passed

![Tests Passed](screenshots/tests-passed.png)

---

## Future Improvements

- 🐳 **Docker** — containerize for one-command deployment
- 🔄 **Alembic migrations** — versioned schema evolution
- 🚦 **Rate limiting** — protect endpoints from abuse
- 🔑 **Role expansion** — granular permissions per resource type
- 📊 **Observability** — structured logging and request tracing

---

<div align="center">
<i>I build things I'd trust with something that matters.</i>
<br><br>
Built by <b>Georgios Panagopoulos</b>
<br>
<a href="https://github.com/GiorgosPanagopoulos"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white"/></a>
<a href="https://linkedin.com/in/gpanagopoulos"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/></a>
<br><br>
☕ Powered by mass amounts of caffeine & mass amounts of curiosity.
</div>
