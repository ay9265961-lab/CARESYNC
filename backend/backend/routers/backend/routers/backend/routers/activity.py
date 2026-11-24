
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import User, ActivityLog, FamilyLink
from backend.dependencies import get_current_user


router = APIRouter(
    prefix="/activity",
    tags=["Activity Logs"]
)


@router.get("/")
def view_activity(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "elderly":
        user_ids = [current_user.id]

    elif current_user.role == "family":
        links = db.query(FamilyLink).filter(
            FamilyLink.family_user_id == current_user.id,
            FamilyLink.status == "approved"
        ).all()

        user_ids = [link.elderly_user_id for link in links]
        user_ids.append(current_user.id)

    else:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to view these activity logs."
        )

    logs = db.query(ActivityLog).filter(
        ActivityLog.user_id.in_(user_ids)
    ).order_by(
        ActivityLog.created_at.desc()
    ).limit(100).all()

    return [
        {
            "id": log.id,
            "user_id": log.user_id,
            "action": log.action,
            "decision": log.decision,
            "details": log.details,
            "created_at": log.created_at
        }
        for log in logs
    ]
