"""
Pydantic schemas for API request/response models.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum


class RoomType(str, Enum):
    LIVING_ROOM = "living_room"
    BEDROOM = "bedroom"
    KITCHEN = "kitchen"
    BATHROOM = "bathroom"
    DINING_ROOM = "dining_room"
    HOME_OFFICE = "home_office"
    BASEMENT = "basement"
    GARAGE = "garage"
    OUTDOOR = "outdoor"
    OTHER = "other"


class StyleType(str, Enum):
    MODERN = "modern"
    TRADITIONAL = "traditional"
    RUSTIC = "rustic"
    MINIMALIST = "minimalist"
    INDUSTRIAL = "industrial"
    BOHEMIAN = "bohemian"
    SCANDINAVIAN = "scandinavian"
    FARMHOUSE = "farmhouse"
    CONTEMPORARY = "contemporary"
    VINTAGE = "vintage"


class DifficultyLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class ProjectStatus(str, Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Intent schemas
class IntentRequest(BaseModel):
    user_input: str
    image_description: Optional[str] = None
    additional_context: Optional[Dict[str, Any]] = None


class UserIntent(BaseModel):
    room_type: RoomType
    style_preference: StyleType
    budget_range: Optional[str] = None
    timeline: Optional[str] = None
    specific_items: List[str] = []
    constraints: List[str] = []
    goals: List[str] = []


# Rendering schemas
class RenderingPrompt(BaseModel):
    style: StyleType
    room_type: RoomType
    description: str
    lighting: str
    color_scheme: List[str]
    focal_points: List[str]


class GeneratedImage(BaseModel):
    prompt: str
    style: StyleType
    image_url: str
    creation_timestamp: str


class RenderingResponse(BaseModel):
    id: int
    prompt: str
    style: str
    image_url: Optional[str]
    description: str
    lighting: str
    color_scheme: List[str]
    focal_points: List[str]
    is_selected: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Project schemas
class ProjectCreate(BaseModel):
    title: str
    description: Optional[str] = None
    room_type: RoomType
    style_preference: StyleType
    budget_range: Optional[str] = None


class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None


class ProjectBase(BaseModel):
    title: str
    description: Optional[str]
    room_type: str
    style_preference: str
    budget_range: Optional[str]
    status: str
    estimated_cost: Optional[float]
    estimated_time: Optional[str]
    difficulty_level: Optional[str]


class Project(ProjectBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ProjectWithDetails(Project):
    renderings: List[RenderingResponse] = []
    user_intent: Optional[Dict[str, Any]] = None


# Material and Tool schemas
class Material(BaseModel):
    name: str
    quantity: str
    estimated_cost: float
    store_suggestion: Optional[str] = None
    alternatives: List[str] = []


class Tool(BaseModel):
    name: str
    required: bool
    rental_option: bool = False
    estimated_cost: Optional[float] = None


class Step(BaseModel):
    step_number: int
    title: str
    description: str
    estimated_time: str
    difficulty: DifficultyLevel
    tools_needed: List[str]
    safety_notes: List[str] = []
    tips: List[str] = []


# Plan schemas
class DecorationPlan(BaseModel):
    project_title: str
    description: str
    room_type: RoomType
    style: StyleType
    total_estimated_cost: float
    estimated_time: str
    difficulty_level: DifficultyLevel
    materials: List[Material]
    tools: List[Tool]
    preparation_steps: List[str]
    installation_steps: List[Step]
    finishing_touches: List[str]
    safety_warnings: List[str] = []
    maintenance_tips: List[str] = []
    alternative_approaches: List[str] = []


class ProjectPlanResponse(BaseModel):
    id: int
    title: str
    description: str
    total_estimated_cost: float
    estimated_time: str
    difficulty_level: str
    materials: List[Dict[str, Any]]
    tools: List[Dict[str, Any]]
    preparation_steps: List[str]
    installation_steps: List[Dict[str, Any]]
    finishing_touches: List[str]
    safety_warnings: List[str]
    maintenance_tips: List[str]
    alternative_approaches: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# Shopping list schemas
class ShoppingList(BaseModel):
    total_estimated_cost: float
    categories: Dict[str, List[Material]]
    store_recommendations: Dict[str, List[str]]
    money_saving_tips: List[str] = []


class ShoppingListResponse(BaseModel):
    id: int
    total_estimated_cost: float
    categories: Dict[str, Any]
    store_recommendations: Dict[str, Any]
    money_saving_tips: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# Session schemas
class RenderingSelectionRequest(BaseModel):
    rendering_index: int


class AgentSessionResponse(BaseModel):
    id: int
    session_id: str
    status: str
    current_step: Optional[str]
    user_input: str
    image_description: Optional[str]
    selected_rendering_index: Optional[int]
    errors: List[str] = []
    messages: List[str] = []
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# Complete session response
class CompleteSessionResponse(BaseModel):
    session_id: str
    project: ProjectWithDetails
    user_intent: UserIntent
    rendering_prompts: List[RenderingPrompt]
    generated_images: List[GeneratedImage]
    selected_rendering: Optional[int]
    decoration_plan: Optional[DecorationPlan]
    shopping_list: Optional[ShoppingList]
    created_at: str
    updated_at: str


# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# Error schemas
class ErrorResponse(BaseModel):
    detail: str
    error_code: Optional[str] = None


class ValidationErrorResponse(BaseModel):
    detail: str
    errors: List[Dict[str, Any]]


# Additional CRUD schemas

# Rendering CRUD schemas
class RenderingCreate(BaseModel):
    project_id: int
    prompt: str
    style: str
    image_url: Optional[str] = None
    description: Optional[str] = None
    lighting: Optional[str] = None
    color_scheme: List[str] = []
    focal_points: List[str] = []


class RenderingUpdate(BaseModel):
    prompt: Optional[str] = None
    style: Optional[str] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    lighting: Optional[str] = None
    color_scheme: Optional[List[str]] = None
    focal_points: Optional[List[str]] = None
    is_selected: Optional[bool] = None


class Rendering(BaseModel):
    id: int
    project_id: int
    prompt: str
    style: str
    image_url: Optional[str]
    is_selected: bool
    description: Optional[str]
    lighting: Optional[str]
    color_scheme: List[str]
    focal_points: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# ProjectPlan CRUD schemas
class ProjectPlanCreate(BaseModel):
    project_id: int
    title: str
    description: Optional[str] = None
    total_estimated_cost: float
    estimated_time: str
    difficulty_level: str
    materials: List[Dict[str, Any]] = []
    tools: List[Dict[str, Any]] = []
    preparation_steps: List[str] = []
    execution_steps: List[Dict[str, Any]] = []
    safety_considerations: List[str] = []
    tips_and_tricks: List[str] = []


class ProjectPlanUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    total_estimated_cost: Optional[float] = None
    estimated_time: Optional[str] = None
    difficulty_level: Optional[str] = None
    materials: Optional[List[Dict[str, Any]]] = None
    tools: Optional[List[Dict[str, Any]]] = None
    preparation_steps: Optional[List[str]] = None
    execution_steps: Optional[List[Dict[str, Any]]] = None
    safety_considerations: Optional[List[str]] = None
    tips_and_tricks: Optional[List[str]] = None


class ProjectPlan(BaseModel):
    id: int
    project_id: int
    title: str
    description: Optional[str]
    total_estimated_cost: float
    estimated_time: str
    difficulty_level: str
    materials: List[Dict[str, Any]]
    tools: List[Dict[str, Any]]
    preparation_steps: List[str]
    execution_steps: List[Dict[str, Any]]
    safety_considerations: List[str]
    tips_and_tricks: List[str]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# ShoppingList CRUD schemas
class ShoppingListCreate(BaseModel):
    project_id: int
    items: List[Dict[str, Any]]
    total_cost: float
    stores: List[Dict[str, Any]] = []
    alternatives: List[Dict[str, Any]] = []


class ShoppingListUpdate(BaseModel):
    items: Optional[List[Dict[str, Any]]] = None
    total_cost: Optional[float] = None
    stores: Optional[List[Dict[str, Any]]] = None
    alternatives: Optional[List[Dict[str, Any]]] = None


class ShoppingList(BaseModel):
    id: int
    project_id: int
    items: List[Dict[str, Any]]
    total_cost: float
    stores: List[Dict[str, Any]]
    alternatives: List[Dict[str, Any]]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


# AgentSession CRUD schemas
class AgentSessionCreate(BaseModel):
    project_id: int
    status: str = "active"
    started_at: datetime
    agent_outputs: Dict[str, Any] = {}


class AgentSessionUpdate(BaseModel):
    status: Optional[str] = None
    ended_at: Optional[datetime] = None
    error_message: Optional[str] = None
    agent_outputs: Optional[Dict[str, Any]] = None


class AgentSession(BaseModel):
    id: int
    project_id: int
    status: str
    started_at: datetime
    ended_at: Optional[datetime]
    error_message: Optional[str]
    agent_outputs: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
