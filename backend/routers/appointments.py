
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import User, Appointment
from backend.schemas import AppointmentCreate, AppointmentResponse
from backend.dependencies import get_current_user
from backend.permissions import evaluate_permission


router = APIRouter(
    prefix="/appointments",
    tags=["Appointment Management"]
)


@router.get("/", response_model=list[AppointmentResponse])
def list_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    decision = evaluate_permission("appointment.list")

    if decision["decision"] != "ALLOW":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=decision["reason"]
        )

    return db.query(Appointment).filter(
        Appointment.owner_id == current_user.id
    ).order_by(Appointment.appointment_time.asc()).all()


@router.post(
    "/",
    response_model=AppointmentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_appointment(
    appointment_data: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    decision = evaluate_permission("appointment.create")

    if decision["decision"] != "ALLOW":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=decision["reason"]
        )

    new_appointment = Appointment(
        title=appointment_data.title,
        appointment_time=appointment_data.appointment_time,
        location=appointment_data.location,
        notes=appointment_data.notes,
        owner_id=current_user.id
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return new_appointment
