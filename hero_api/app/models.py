from typing import Optional

from sqlmodel import Field, SQLModel


# --- Table Models ---

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    is_admin: bool = False


class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, min_length=3)
    power: str = Field(min_length=3)
    level: int = Field(default=1, ge=1, le=100)
    active: bool = True


class Mission(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(min_length=5)
    difficulty: int = Field(ge=1, le=10)
    completed: bool = False
    hero_id: int = Field(foreign_key="hero.id")


# --- Schemas ---

class UserCreate(SQLModel):
    username: str
    password: str


class UserResponse(SQLModel):
    id: int
    username: str
    is_admin: bool


class HeroCreate(SQLModel):
    name: str
    power: str
    level: int = 1
    active: bool = True


class HeroUpdate(SQLModel):
    name: Optional[str] = None
    power: Optional[str] = None
    level: Optional[int] = None
    active: Optional[bool] = None


class HeroResponse(SQLModel):
    id: int
    name: str
    power: str
    level: int
    active: bool


class MissionCreate(SQLModel):
    title: str
    difficulty: int
    hero_id: int


class MissionUpdate(SQLModel):
    title: Optional[str] = None
    difficulty: Optional[int] = None
    completed: Optional[bool] = None
    hero_id: Optional[int] = None


class MissionResponse(SQLModel):
    id: int
    title: str
    difficulty: int
    completed: bool
    hero_id: int
