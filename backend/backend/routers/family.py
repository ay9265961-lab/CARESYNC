
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import User, FamilyLink
from backend.dependencies import get_current_user


router = APIRouter(
    prefix="/family",
    tags=["Family Management"]
)


@router.post("/request/{elderly_user_id}")
def request_family_link(
    elderly_user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "family":
        raise HTTPException(
            status_code=403,
            detail="Only family accounts can request a family link."
        )

    elderly_user = db.query(User).filter(
        User.id == elderly_user_id,
        User.role == "elderly",
        User.is_active == True
    ).first()

    if not elderly_user:
        raise HTTPException(
            status_code=404,
            detail="Active elderly user not found."
        )

    existing_link = db.query(FamilyLink).filter(
        FamilyLink.elderly_user_id == elderly_user_id,
        FamilyLink.family_user_id == current_user.id
    ).first()

    if existing_link:
        raise HTTPException(
            status_code=409,
            detail="A family link request or connection already exists."
        )

    link = FamilyLink(
        elderly_user_id=elderly_user_id,
        family_user_id=current_user.id,
        status="pending"
    )

    db.add(link)
    db.commit()
    db.refresh(link)

    return {
        "message": "Family link request submitted.",
        "request_id": link.id,
        "status": link.status
    }


@router.get("/requests")
def view_family_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "elderly":
        raise HTTPException(
            status_code=403,
            detail="Only elderly users can view incoming requests."
        )

    requests = db.query(FamilyLink).filter(
        FamilyLink.elderly_user_id == current_user.id,
        FamilyLink.status == "pending"
    ).all()

    return [
        {
            "request_id": link.id,
            "family_member": db.query(User).filter(
                User.id == link.family_user_id
            ).first().name,
            "family_user_id": link.family_user_id,
            "status": link.status
        }
        for link in requests
    ]


@router.post("/approve/{request_id}")
def approve_family_link(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "elderly":
        raise HTTPException(
            status_code=403,
            detail="Only the elderly account can approve this request."
        )

    link = db.query(FamilyLink).filter(
        FamilyLink.id == request_id,
        FamilyLink.elderly_user_id == current_user.id,
        FamilyLink.status == "pending"
    ).first()

    if not link:
        raise HTTPException(
            status_code=404,
            detail="Pending family request not found."
        )

    link.status = "approved"
    db.commit()

    return {
        "message": "Family connection approved.",
        "status": link.status
    }
