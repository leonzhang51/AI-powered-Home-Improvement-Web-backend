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
