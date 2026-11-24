
import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import (
    User,
    Medicine,
    ApprovalRequest,
    FamilyLink,
    ActivityLog
)
from backend.dependencies import get_current_user


router = APIRouter(
    prefix="/approvals",
    tags=["Family Approvals"]
)


def check_family_access(
    elderly_user_id: int,
    family_user_id: int,
    db: Session
):
    link = db.query(FamilyLink).filter(
        FamilyLink.elderly_user_id == elderly_user_id,
        FamilyLink.family_user_id == family_user_id,
        FamilyLink.status == "approved"
    ).first()

    return link is not None


@router.get("/pending")
def view_pending_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "family":
        raise HTTPException(
            status_code=403,
            detail="Only family members can view approval requests."
        )

    links = db.query(FamilyLink).filter(
        FamilyLink.family_user_id == current_user.id,
        FamilyLink.status == "approved"
    ).all()

    elderly_ids = [link.elderly_user_id for link in links]

    if not elderly_ids:
        return []

    requests = db.query(ApprovalRequest).filter(
        ApprovalRequest.requested_by.in_(elderly_ids),
        ApprovalRequest.status == "pending"
    ).all()

    return [
        {
            "request_id": request.id,
            "action": request.action,
            "description": request.description,
            "requested_by": request.requested_by,
            "created_at": request.created_at
        }
        for request in requests
    ]


@router.post("/{request_id}/approve")
def approve_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "family":
        raise HTTPException(
            status_code=403,
            detail="Only family members can approve requests."
        )

    request = db.query(ApprovalRequest).filter(
        ApprovalRequest.id == request_id,
        ApprovalRequest.status == "pending"
    ).with_for_update().first()

    if not request:
        raise HTTPException(
            status_code=404,
            detail="Pending request not found."
        )

    if not check_family_access(
        request.requested_by,
        current_user.id,
        db
    ):
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to approve this request."
        )

    # A family approval cannot override a prohibited action.
    if request.action != "medicine.record.add":
        raise HTTPException(
            status_code=403,
            detail="This action is not supported by the approval workflow."
        )

    try:
        medicine_data = json.loads(request.description or "{}")

        name = medicine_data["name"]
        stock = medicine_data["stock"]
        daily_consumption = medicine_data["daily_consumption"]

        if (
            not isinstance(name, str)
            or not name.strip()
            or type(stock) is not int
            or type(daily_consumption) is not int
            or stock < 0
            or daily_consumption <= 0
        ):
            raise ValueError("Invalid medicine details.")

    except (ValueError, TypeError, KeyError):
        raise HTTPException(
            status_code=400,
            detail="Invalid medicine request data."
        )

    medicine = Medicine(
        name=name.strip(),
        stock=stock,
        daily_consumption=daily_consumption,
        owner_id=request.requested_by
    )

    request.status = "approved"
    request.approved_by = current_user.id

    db.add(medicine)

    db.add(ActivityLog(
        user_id=current_user.id,
        action=f"Approved medicine addition: {name.strip()}",
        decision="ALLOW",
        details=f"Approval request ID: {request.id}"
    ))

    db.commit()

    return {
        "message": "Request approved and medicine record created.",
        "request_id": request.id,
        "status": request.status
    }


@router.post("/{request_id}/reject")
def reject_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "family":
        raise HTTPException(
            status_code=403,
            detail="Only family members can reject requests."
        )

    request = db.query(ApprovalRequest).filter(
        ApprovalRequest.id == request_id,
        ApprovalRequest.status == "pending"
    ).first()

    if not request:
        raise HTTPException(
            status_code=404,
            detail="Pending request not found."
        )

    if not check_family_access(
        request.requested_by,
        current_user.id,
        db
    ):
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to reject this request."
        )

    request.status = "rejected"
    request.approved_by = current_user.id

    db.add(ActivityLog(
        user_id=current_user.id,
        action=f"Rejected approval request {request.id}",
        decision="BLOCK",
        details=f"Action: {request.action}"
    ))

    db.commit()

    return {
        "message": "Request rejected.",
        "request_id": request.id,
        "status": request.status
    }
