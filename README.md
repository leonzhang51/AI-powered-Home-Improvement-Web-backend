
---

## 📁 `home-diy-api/README.md`

```markdown
# HomeDIY API

This is the **backend** of the HomeDIY MVP — built with **FastAPI** and **PostgreSQL**, connected to a separate `home-diy-agents` microservice for AI logic.

## 🌟 Purpose

This API powers the frontend and coordinates between:
- User input (text or image)
- Agent microservice (`home-diy-agents`) for AI processing
- Project database (e.g., plans, materials, user sessions)

## 🧱 Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [SQLAlchemy or Tortoise ORM](https://www.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- Optional: [Celery](https://docs.celeryq.dev/) for async task queuing

## 📁 Folder Structure

app/
├── main.py # FastAPI startup
├── api/routes.py # Endpoints for /intent, /renderings, /plan
├── db/ # DB models, CRUD logic
├── services/ # Business logic, agent-client interface
├── schemas/ # Pydantic models
tests/

## 🔁 External Dependencies

- Agent service (`home-diy-agents`) runs separately and is queried via HTTP
- Optional: S3/Cloudinary for image uploads

## 🚀 Expected Behavior (Copilot Prompting)

> "Write a POST endpoint `/intent` that sends user input to the agent service and returns structured room/style info."

> "Add a `/plan` endpoint that stores the generated decoration plan into the DB."

## 🛠 Local Dev

```bash
uvicorn app.main:app --reload

🔄 API Endpoints
Method	Endpoint	Description
POST	/intent	Sends user input to AI agent
GET	/project/:id	Get saved project plan

🧪 TODO
 Add caching layer for repeated renderings

 Add auth middleware for user profiles

 Connect to agents over HTTP (mock first)


