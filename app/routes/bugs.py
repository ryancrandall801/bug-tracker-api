from fastapi import APIRouter, status
from app.models import BugCreate, BugResponse

router = APIRouter(prefix="/bugs", tags=["bugs"])

bugs_db = []
next_bug_id = 1


@router.post("", response_model=BugResponse, status_code=status.HTTP_201_CREATED)
def create_bug(bug: BugCreate):
    global next_bug_id

    new_bug = {
        "id": next_bug_id,
        "title": bug.title,
        "description": bug.description,
        "priority": bug.priority,
        "status": "open",
    }

    bugs_db.append(new_bug)
    next_bug_id += 1

    return new_bug