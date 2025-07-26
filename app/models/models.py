"""
Database models for the Home DIY application.
"""
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class User(Base):
    """User model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    projects = relationship("Project", back_populates="user")


class Project(Base):
    """Project model for DIY projects."""
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    room_type = Column(String, nullable=False)
    style_preference = Column(String, nullable=False)
    budget_range = Column(String)
    status = Column(String, default="draft")  # draft, in_progress, completed
    user_intent = Column(JSON)  # Store the extracted intent
    
    # Cost and time estimates
    estimated_cost = Column(Float)
    estimated_time = Column(String)
    difficulty_level = Column(String)
    
    # Foreign keys
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="projects")
    renderings = relationship("Rendering", back_populates="project")
    plans = relationship("ProjectPlan", back_populates="project")
    shopping_lists = relationship("ShoppingList", back_populates="project")
    sessions = relationship("AgentSession", back_populates="project")


class Rendering(Base):
    """Rendering model for design options."""
    __tablename__ = "renderings"
    
    id = Column(Integer, primary_key=True, index=True)
    prompt = Column(Text, nullable=False)
    style = Column(String, nullable=False)
    image_url = Column(String)
    is_selected = Column(Boolean, default=False)
    
    # Rendering details
    description = Column(Text)
    lighting = Column(String)
    color_scheme = Column(JSON)  # Array of colors
    focal_points = Column(JSON)  # Array of focal points
    
    # Foreign keys
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="renderings")


class ProjectPlan(Base):
    """Project plan model with detailed instructions."""
    __tablename__ = "project_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    
    # Cost and time details
    total_estimated_cost = Column(Float, nullable=False)
    estimated_time = Column(String, nullable=False)
    difficulty_level = Column(String, nullable=False)
    
    # Plan content (stored as JSON)
    materials = Column(JSON)  # List of materials
    tools = Column(JSON)  # List of tools
    preparation_steps = Column(JSON)  # List of preparation steps
    execution_steps = Column(JSON)  # List of execution steps  
    safety_considerations = Column(JSON)  # List of safety considerations
    tips_and_tricks = Column(JSON)  # List of tips and tricks
    
    # Foreign keys
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="plans")


class ShoppingList(Base):
    """Shopping list model."""
    __tablename__ = "shopping_lists"
    
    id = Column(Integer, primary_key=True, index=True)
    items = Column(JSON, nullable=False)  # List of shopping items
    total_cost = Column(Float, nullable=False)
    stores = Column(JSON)  # Store recommendations
    alternatives = Column(JSON)  # Alternative options
    
    # Foreign keys
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="shopping_lists")


class AgentSession(Base):
    """Agent session model to track AI processing."""
    __tablename__ = "agent_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, nullable=False)  # active, completed, failed
    started_at = Column(DateTime(timezone=True), nullable=False)
    ended_at = Column(DateTime(timezone=True))
    error_message = Column(Text)
    agent_outputs = Column(JSON)  # Store agent processing results
    
    # Foreign keys
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="sessions")
