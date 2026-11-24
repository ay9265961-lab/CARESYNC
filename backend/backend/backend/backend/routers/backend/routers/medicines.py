
import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import User, Medicine, ApprovalRequest
from backend.schemas import MedicineCreate, MedicineResponse
from backend.dependencies import get_current_user
from backend.permissions import evaluate_permission


router = APIRouter(
    prefix="/medicines",
    tags=["Medicine Management"]
)


@router.get("/", response_model=list[MedicineResponse])
def list_medicines(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    decision = evaluate_permission("medicine.list")

    if decision["decision"] != "ALLOW":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=decision["reason"]
        )

    return db.query(Medicine).filter(
        Medicine.owner_id == current_user.id
    ).all()


@router.post("/request-add")
def request_add_medicine(
    medicine_data: MedicineCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    decision = evaluate_permission("medicine.record.add")

    if decision["decision"] == "BLOCK":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=decision["reason"]
        )

    if decision["decision"] == "ASK":
        request = ApprovalRequest(
            action="medicine.record.add",
            description=json.dumps(
                medicine_data.model_dump()
            ),
            status="pending",
            requested_by=current_user.id
        )

        db.add(request)
        db.commit()
        db.refresh(request)

        return {
            "decision": "ASK",
            "message": "Medicine addition requires family approval.",
            "request_id": request.id,
            "status": request.status
        }

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Unexpected permission decision."
    )
