
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# -------------------------
# USER SCHEMAS
# -------------------------

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=8)
    role: str = "elderly"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# MEDICINE SCHEMAS
# -------------------------

class MedicineCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    stock: int = Field(ge=0)
    daily_consumption: int = Field(gt=0)


class MedicineResponse(BaseModel):
    id: int
    name: str
    stock: int
    daily_consumption: int
    refill_date: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# APPOINTMENT SCHEMAS
# -------------------------

class AppointmentCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    appointment_time: datetime
    location: str | None = None
    notes: str | None = None


class AppointmentResponse(BaseModel):
    id: int
    title: str
    appointment_time: datetime
    location: str | None = None
    notes: str | None = None

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# APPROVAL SCHEMAS
# -------------------------

class ApprovalCreate(BaseModel):
    action: str = Field(min_length=1, max_length=150)
    description: str | None = None


class ApprovalResponse(BaseModel):
    id: int
    action: str
    description: str | None = None
    status: str

    model_config = ConfigDict(from_attributes=True)
