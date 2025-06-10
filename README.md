# 🚀 HomeImproveAI - Backend

![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?logo=fastapi)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16+-4169E1?logo=postgresql)
![License](https://img.shields.io/badge/License-MIT-blue)

**AI-Powered Home Improvement Backend Service**  
RESTful API for generating home design renderings, material lists, and project plans.

## ✨ Features

- 🖼️ **AI Rendering Pipeline**: Process text/image inputs to generate design options
- 🛒 **Smart Material Lists**: Automated shopping list generation with quantities
- ⏱️ **Cost & Time Estimation**: Real-world price scraping and time calculations
- 🔗 **LangChain Integration**: AI agent workflows for project planning
- 🔐 **JWT Authentication**: Secure user endpoints
- 📊 **PostgreSQL Database**: Persistent storage for projects and users

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.11+)
- **Database**: [PostgreSQL](https://www.postgresql.org/) + [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
- **AI Integration**: [LangChain](https://www.langchain.com/) + [LangSmith](https://smith.langchain.com/)
- **Authentication**: [OAuth2 with JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- **Vector Search**: [pgvector](https://github.com/pgvector/pgvector) (for design similarity)
- **Testing**: [pytest](https://docs.pytest.org/) + [HTTPX](https://www.python-httpx.org/)

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 16+ (with pgvector extension)
- Redis (for caching, optional)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/homeimproveai-backend.git
   cd homeimproveai-backend
2. Create and activate virtual environment:
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
3. Install dependencies:
   pip install -r requirements.txt
4. Set up environment variables:
   cp .env.example .env
   Edit .env with your:

   Database credentials
   
   OpenAI/LangChain API keys
   
   JWT secret key
5. Run database migrations:
   alembic upgrade head
6. Start the server:
   uvicorn app.main:app --reload
Access docs at: http://localhost:8000/docs
🏗️ Project Structure
homeimproveai-backend/
├── app/
│   ├── core/              # Configurations and utilities
│   ├── db/                # Database models and migrations
│   ├── schemas/           # Pydantic models
│   ├── routes/            # API endpoints
│   │   ├── auth.py        # Authentication routes
│   │   ├── renderings.py  # AI design generation
│   │   └── projects.py    # Project management
│   ├── agents/            # LangChain agents
│   │   ├── materials.py   # Material list generator
│   │   └── cost.py        # Cost estimator
│   └── main.py            # FastAPI app instance
├── tests/                 # Test cases
├── alembic/               # Database migrations
├── scripts/               # Utility scripts
└── requirements.txt       # Dependencies
📡 API Endpoints
Endpoint	Method	Description
/api/v1/renderings	POST	Generate design renderings from input
/api/v1/projects	GET	Get project details
/api/v1/materials	GET	Get material list for project
/api/v1/auth/login	POST	User authentication
View full API documentation: http://localhost:8000/docs

🧪 Testing
Run all tests:
pytest
With coverage report:
pytest --cov=app --cov-report=html
🐳 Docker Deployment
Build the image:
docker build -t homeimproveai-backend .
Run with PostgreSQL:
docker-compose up -d

🧠 AI Agent Deep Dive
LangChain Agent Workflow
# Example agent pipeline (app/agents/render_agent.py)
from langchain_core.agents import AgentExecutor
from langchain_community.tools import Tool

def generate_design(input: str) -> str:
    # 1. Style extraction
    style_chain = LLMChain(llm=ChatOpenAI(), prompt=style_prompt)
    
    # 2. Material suggestion
    materials_agent = create_react_agent(llm, tools, materials_prompt)
    
    # 3. Cost estimation
    cost_tool = Tool(
        name="cost_calculator",
        func=get_hardware_store_prices,
        description="Fetches material costs from Home Depot API"
    )
    
    return AgentExecutor(agents=[style_chain, materials_agent], tools=[cost_tool])
    🗃️ Database Schema Highlights
    -- Key tables (app/db/models.py)
CREATE TABLE projects (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    initial_prompt TEXT,
    style VARCHAR(32)  -- 'modern', 'rustic', etc.
);

CREATE TABLE ai_renderings (
    id SERIAL PRIMARY KEY,
    project_id UUID REFERENCES projects(id),
    image_url TEXT,
    embedding vector(1536)  -- pgvector storage
);

CREATE TABLE material_lists (
    id UUID PRIMARY KEY,
    project_id UUID REFERENCES projects(id),
    items JSONB  -- { "paint": { "quantity": "2 gallons", "sku": "HD-123" } }
);

🛡️ Authentication Flow
sequenceDiagram
    Frontend->>Backend: POST /auth/login (email, password)
    Backend->>DB: Verify credentials
    DB-->>Backend: User record
    Backend->>Backend: Generate JWT
    Backend-->>Frontend: { access_token, expires_in }
    Frontend->>Backend: Authorization: Bearer <token>

   🚢 Deployment Strategies
   Docker Compose (Full Stack)
   # docker-compose.prod.yml
services:
  backend:
    build: .
    ports: ["8000:8000"]
    depends_on:
      - postgres
      - redis
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/main

  postgres:
    image: postgres:16
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password

   📊 Monitoring Setup
LangSmith Tracing:

python
# Enable in app/main.py
from langsmith import Client

client = Client(
    api_url="https://api.smith.langchain.com",
    api_key=os.getenv("LANGSMITH_API_KEY")
)
🧪 Testing Suite Examples
Integration Test:

python
# tests/test_renderings.py
@pytest.mark.asyncio
async def test_rendering_generation(test_client):
    response = await test_client.post(
        "/api/v1/renderings",
        json={"prompt": "modern kitchen"},
        headers={"Authorization": f"Bearer {TEST_TOKEN}"}
    )
    assert response.status_code == 200
    assert len(response.json()["renderings"]) == 4
🔄 CI/CD Pipeline
.github/workflows/deploy.yml:

yaml
name: Deploy
on: push

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker-compose -f docker-compose.ci.yml build
      - run: docker-compose -f docker-compose.ci.yml up -d
      - run: pytest --cov=app
🌐 API Response Example
POST /api/v1/renderings:

json
{
  "status": "success",
  "data": {
    "renderings": [
      {
        "url": "https://cdn.example.com/renders/1.jpg",
        "style": "modern",
        "materials": [
          {"name": "wall paint", "quantity": "2 gallons"},
          {"name": "floor tiles", "quantity": "50 sq ft"}
        ]
      }
    ],
    "cost_estimate": {
      "total": 1245.50,
      "breakdown": {...}
    }
  }
}
