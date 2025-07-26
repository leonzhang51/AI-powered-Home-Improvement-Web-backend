# 🏠 Home DIY - FastAPI Backend

This is the **backend API** for the Home DIY application — built with **FastAPI** and **PostgreSQL**, integrated with the AI agents system for intelligent home improvement planning.

## 🌟 Purpose

This API powers the frontend and coordinates between:

- User authentication and project management
- AI agents system for project processing
- PostgreSQL database for data persistence
- Frontend React/Next.js application

## 🧱 Tech Stack

- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[PostgreSQL](https://www.postgresql.org/)** - Robust relational database
- **[SQLAlchemy](https://www.sqlalchemy.org/)** - Python SQL toolkit and ORM
- **[Pydantic](https://docs.pydantic.dev/)** - Data validation using Python type hints
- **[Alembic](https://alembic.sqlalchemy.org/)** - Database migration tool
- **[JWT](https://jwt.io/)** - JSON Web Tokens for authentication

## 📁 Project Structure

```
AI-powered-Home-Improvement-Web-backend/
├── main.py                    # FastAPI application startup
├── requirements.txt           # Python dependencies
├── alembic.ini               # Database migration configuration
├── app/
│   ├── __init__.py
│   ├── api/                  # API route handlers
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── users.py         # User management
│   │   ├── projects.py      # Project CRUD operations
│   │   ├── renderings.py    # Design rendering management
│   │   ├── project_plans.py # Project planning endpoints
│   │   ├── shopping_lists.py # Shopping list management
│   │   └── ai_agents.py     # AI agents integration
│   ├── core/                # Core configuration
│   │   ├── config.py        # Application settings
│   │   └── security.py      # Authentication & security
│   ├── crud/                # Database operations
│   │   ├── base.py          # Base CRUD operations
│   │   └── crud_*.py        # Model-specific CRUD
│   ├── db/                  # Database configuration
│   │   └── database.py      # Database connection setup
│   ├── models/              # SQLAlchemy models
│   │   └── models.py        # Database table definitions
│   ├── schemas/             # Pydantic schemas
│   │   └── schemas.py       # API request/response models
│   └── services/            # Business logic
│       ├── ai_agents_service.py # AI integration service
│       └── project_service.py   # Project management logic
├── alembic/                 # Database migrations
└── tests/                   # Unit and integration tests
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.11+**
- **PostgreSQL** (running and accessible)
- **AI Agents System** (from companion repository)
- **Next.js Frontend** (optional, for full system)

### 1. Environment Setup

```bash
# Clone and navigate to the backend directory
cd AI-powered-Home-Improvement-Web-backend

# Install Python dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your database credentials and secrets
```

### 2. Database Setup

```bash
# Ensure PostgreSQL is running
# Create database: home_diy_db

# Run database migrations
alembic upgrade head
```

### 3. Start the Backend Server

```bash
# Start the FastAPI development server
python3 -m uvicorn main:app --reload --host localhost --port 8000
```

The API will be available at:

- **API Server**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🔧 Complete System Setup

To run the full DIY Home Improvement application:

### 1. Start AI Agents System

```bash
cd ../AI-Agents-LangChain-LangGraph-LangSmith
pip install -r requirements.txt
# Test the system
python3 -c "from graphs.diy_workflow import DIYWorkflow; print('✅ AI Agents Ready!')"
```

### 2. Start FastAPI Backend (this repository)

```bash
cd ../AI-powered-Home-Improvement-Web-backend
pip install -r requirements.txt
alembic upgrade head
python3 -m uvicorn main:app --reload --host localhost --port 8000
```

### 3. Start Next.js Frontend

```bash
cd ../ai-powered-home-improvement-web-frontend
npm install
npm run dev
```

### System Verification

```bash
# Check all components
curl http://localhost:8000/health    # Backend health
curl http://localhost:3000           # Frontend
open http://localhost:8000/docs      # API documentation
```

## 🔄 API Endpoints

### Authentication

- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login/access-token` - User login

### Users

- `GET /api/v1/users/me` - Get current user profile
- `GET /api/v1/users/me/stats` - Get user statistics

### Projects

- `GET/POST /api/v1/projects` - List/create projects
- `GET /api/v1/projects/{id}` - Get specific project
- `GET /api/v1/projects/{id}/summary` - Get project summary

### AI Integration

- `POST /api/v1/ai-agents/process-project` - Process project through AI agents
- `GET /api/v1/renderings` - Get design renderings
- `POST /api/v1/renderings/{id}/select` - Select preferred rendering

### Project Planning

- `GET/POST /api/v1/project-plans` - Project plans management
- `GET/POST /api/v1/shopping-lists` - Shopping lists management

## 🧪 System Status

### ✅ Completed Features

- Complete authentication system with JWT
- Full CRUD operations for all entities
- Database models and migrations
- AI agents integration service
- API documentation with FastAPI/OpenAPI
- PostgreSQL database integration
- User management and project tracking
- Design rendering management
- Project planning and shopping lists

### 🔮 Future Enhancements

- Real-time project updates with WebSockets
- Image upload integration (S3/Cloudinary)
- Caching layer for improved performance
- Advanced error handling and logging
- Rate limiting and API versioning
- Background task processing with Celery

## 🧪 Testing

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

## 📊 Database Schema

The system includes models for:

- **Users** - Authentication and profile data
- **Projects** - DIY project information
- **Renderings** - AI-generated design concepts
- **ProjectPlans** - Detailed implementation plans
- **ShoppingLists** - Material and cost organization
- **AgentSessions** - AI processing session tracking

## 🔗 Integration

This backend integrates with:

- **AI Agents System** - LangChain/LangGraph workflow processing
- **Next.js Frontend** - React-based user interface
- **PostgreSQL Database** - Data persistence and relationships
- **External APIs** - Image generation and material databases (future)

## 🤝 Contributing

1. Follow FastAPI best practices
2. Use Pydantic for all data validation
3. Write tests for new endpoints
4. Update API documentation
5. Follow the existing project structure

## 📄 License

Part of the Home DIY AI-powered home improvement application suite.
