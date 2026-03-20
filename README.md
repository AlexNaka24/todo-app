# ✅ Todo App API

A fully-featured **RESTful API** for managing personal todo lists, built with **FastAPI** and **PostgreSQL**. Supports JWT-based authentication, role-based access control, and full CRUD operations.

---

## 🚀 Tech Stack

| Layer | Technology |
|-------|-----------|
| Framework | [FastAPI](https://fastapi.tiangolo.com/) |
| Language | Python 3.11+ |
| Database | PostgreSQL (via SQLAlchemy ORM) |
| Migrations | Alembic |
| Auth | JWT (JSON Web Tokens) with `python-jose` |
| Password Hashing | `passlib` with `bcrypt` |
| Validation | Pydantic v2 |
| Server | Uvicorn (ASGI) |

---

## 📁 Project Structure

```
todo-app/
├── main.py                  # App entry point, router registration
├── database.py              # SQLAlchemy engine, session, and Base
├── models.py                # ORM models (User, Todos)
├── alembic.ini              # Alembic configuration
├── alembic/
│   └── versions/            # Migration scripts
├── routers/
│   ├── auth.py              # Registration, login, JWT logic
│   ├── todos.py             # CRUD operations for todos
│   ├── users.py             # Profile and password management
│   └── admin.py             # Admin-only endpoints
├── schemas/
│   ├── todo_request.py      # Pydantic schema for todo creation/update
│   ├── user_request.py      # Pydantic schema for user registration
│   ├── user_verification.py # Pydantic schema for password change
│   └── token_squema.py      # Pydantic schema for JWT token response
├── test/
│   └── test_main.py         # Tests
├── conftest.py              # pytest configuration
└── .env                     # Environment variables (not committed)
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/todo-app.git
cd todo-app
```

### 2. Create and activate a virtual environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install fastapi uvicorn sqlalchemy psycopg2-binary alembic python-dotenv passlib[bcrypt] python-jose[cryptography]
```

> ⚠️ **Note on bcrypt compatibility:** `passlib 1.7.4` is incompatible with `bcrypt >= 4.0.0`. Install a compatible version:
> ```bash
> pip install "bcrypt==3.2.2"
> ```

### 4. Configure the database

Create a `.env` file in the project root:
```env
DATABASE_URL="postgresql://your_user:your_password@localhost:5432/your_db_name"
```

#### Option A — Run PostgreSQL with Docker (recommended)
```bash
docker run --name todo-postgres \
  -e POSTGRES_USER=your_user \
  -e POSTGRES_PASSWORD=your_password \
  -e POSTGRES_DB=your_db_name \
  -v /your/local/path:/var/lib/postgresql/data \
  -p 5432:5432 \
  -d postgres
```

#### Option B — Use an existing PostgreSQL installation
Make sure the database exists and update `.env` accordingly.

### 5. Apply database migrations
```bash
alembic upgrade head
```

### 6. Run the application
```bash
uvicorn main:app --reload
```

The API will be available at **http://127.0.0.1:8000**

### 7. Interactive docs
FastAPI automatically generates interactive documentation:
- **Swagger UI** → http://127.0.0.1:8000/docs
- **ReDoc** → http://127.0.0.1:8000/redoc

---

## 🗄️ Database Schema

### `users` table
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PK, autoincrement |
| username | STRING | UNIQUE, indexed |
| first_name | STRING | — |
| last_name | STRING | — |
| email | STRING | UNIQUE, indexed |
| hashed_password | STRING | — |
| role | STRING | `"admin"` or `"user"` |
| is_active | BOOLEAN | default `true` |
| phone_number | STRING | nullable |

### `todos` table
| Column | Type | Constraints |
|--------|------|-------------|
| id | INTEGER | PK, autoincrement |
| title | STRING | indexed |
| description | STRING | — |
| priority | INTEGER | 1–5, indexed |
| complete | BOOLEAN | default `false`, indexed |
| owner_id | INTEGER | FK → `users.id` |

---

## 🔐 Authentication

The API uses **OAuth2 with JWT Bearer tokens**. All protected endpoints require an `Authorization: Bearer <token>` header.

### Flow

```
1. Register  →  POST /auth/create-user
2. Login     →  POST /auth/token          ← returns JWT
3. Use token →  Authorization: Bearer <token>
```

Tokens expire after **30 minutes**.

---

## 📡 API Reference

### 🔑 Auth — `/auth`

#### Register a new user
```http
POST /auth/create-user
Content-Type: application/json

{
  "username": "johndoe",
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "secret123",
  "role": "user",
  "is_active": true,
  "phone_number": "1234567890"
}
```

**Response `201 Created`**
```json
{
  "message": "User created successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "role": "user",
    "is_active": true
  }
}
```

---

#### Login
```http
POST /auth/token
Content-Type: application/x-www-form-urlencoded

username=johndoe&password=secret123
```

**Response `200 OK`**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### ✅ Todos — `/todos`

> All endpoints require authentication.

#### Get all your todos
```http
GET /todos
Authorization: Bearer <token>
```

**Response `200 OK`**
```json
[
  {
    "id": 1,
    "title": "Buy groceries for the week",
    "description": "Milk, eggs, bread, and vegetables",
    "priority": 2,
    "complete": false,
    "owner_id": 1
  }
]
```

> **Note:** Users with the `admin` role receive **all** todos from all users.

---

#### Get todo by ID
```http
GET /todos/{todo_id}
Authorization: Bearer <token>
```

**Response `200 OK`**
```json
{
  "id": 1,
  "title": "Buy groceries for the week",
  "description": "Milk, eggs, bread, and vegetables",
  "priority": 2,
  "complete": false,
  "owner_id": 1
}
```

**Response `404 Not Found`**
```json
{ "detail": "Todo with id 99 not found" }
```

---

#### Get todos by priority
```http
GET /todos/priority/{todo_priority}
Authorization: Bearer <token>
```
Priority must be between **1 and 5**.

**Response `200 OK`**
```json
[
  {
    "id": 3,
    "title": "Finish the project report",
    "description": "Complete all sections and send to manager",
    "priority": 5,
    "complete": false,
    "owner_id": 1
  }
]
```

---

#### Create a new todo
```http
POST /todos/create-todo
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Finish the project report",
  "description": "Complete all sections and send to manager",
  "priority": 5,
  "complete": false
}
```

**Validation rules:**
| Field | Rule |
|-------|------|
| title | 10–50 characters |
| description | 10–200 characters |
| priority | Integer 0–5 |
| complete | Boolean (default `false`) |

**Response `201 Created`**
```json
{
  "message": "Todo with id 3 created successfully",
  "todo": {
    "id": 3,
    "title": "Finish the project report",
    "description": "Complete all sections and send to manager",
    "priority": 5,
    "complete": false,
    "owner_id": 1
  }
}
```

---

#### Update a todo
```http
PUT /todos/update-todo/{todo_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Finish the project report",
  "description": "Complete all sections and send to manager",
  "priority": 5,
  "complete": true
}
```

**Response `200 OK`**
```json
{
  "message": "Todo with id 3 updated successfully",
  "todo": {
    "id": 3,
    "title": "Finish the project report",
    "description": "Complete all sections and send to manager",
    "priority": 5,
    "complete": true,
    "owner_id": 1
  }
}
```

---

#### Delete a todo
```http
DELETE /todos/delete-todo/{todo_id}
Authorization: Bearer <token>
```

**Response `200 OK`**
```json
{ "message": "Todo with id 3 deleted successfully" }
```

---

### 👤 User — `/user`

> All endpoints require authentication.

#### Get current user profile
```http
GET /user/me
Authorization: Bearer <token>
```

**Response `200 OK`**
```json
{
  "username": "johndoe",
  "id": 1,
  "role": "user"
}
```

---

#### Change password
```http
PUT /user/change-password
Authorization: Bearer <token>
Content-Type: application/json

{
  "current_password": "secret123",
  "new_password": "newsecret456"
}
```

**Response `200 OK`**
```json
{ "message": "Password changed successfully" }
```

**Response `401 Unauthorized`**
```json
{ "detail": "Incorrect password" }
```

---

### 🛡️ Admin — `/admin`

> All endpoints require authentication and `role: "admin"`.

#### Get all todos (all users)
```http
GET /admin/todos
Authorization: Bearer <admin_token>
```

#### Get all users
```http
GET /admin/users
Authorization: Bearer <admin_token>
```

#### Get user by ID
```http
GET /admin/users/{user_id}
Authorization: Bearer <admin_token>
```

#### Get user by username
```http
GET /admin/users/username/{username}
Authorization: Bearer <admin_token>
```

#### Delete user by ID
```http
DELETE /admin/users/delete/{user_id}
Authorization: Bearer <admin_token>
```
> Deletes the user **and all their todos** in a single transaction.

---

## ❌ Error Responses

| Status Code | Scenario |
|-------------|----------|
| `401 Unauthorized` | Missing, expired, or invalid JWT token |
| `401 Unauthorized` | Wrong username or password on login |
| `401 Unauthorized` | Non-admin accessing an admin endpoint |
| `404 Not Found` | Todo or user does not exist |
| `422 Unprocessable Entity` | Request body fails Pydantic validation |

**Example `422` response:**
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "title"],
      "msg": "String should have at least 10 characters",
      "input": "Buy milk"
    }
  ]
}
```

---

## 🔒 Security Notes

- Passwords are hashed using **bcrypt** and never stored in plain text.
- JWT tokens are signed with a secret key using the **HS256** algorithm.
- Each todo is scoped to its owner — users can only access their own data.
- Admin role grants elevated access but is not automatically assigned; it must be set explicitly during user creation.
- The `.env` file is excluded from version control via `.gitignore` to protect database credentials.

---

## 🗃️ Database Migrations

This project uses **Alembic** to manage schema changes.

```bash
# Apply all pending migrations
alembic upgrade head

# Roll back the last migration
alembic downgrade -1

# Check current migration status
alembic current

# Create a new migration (auto-detect model changes)
alembic revision --autogenerate -m "description of change"
```

---

## 🧪 Running Tests

```bash
pytest test/
```

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).
