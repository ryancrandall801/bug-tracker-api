from fastapi import APIRouter, HTTPException, status
from app.models import BugCreate, BugResponse, BugUpdate

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


@router.get("", response_model=list[BugResponse])
def get_bugs():
    return bugs_db


@router.get("/{bug_id}", response_model=BugResponse)
def get_bug_by_id(bug_id: int):
    for bug in bugs_db:
        if bug["id"] == bug_id:
            return bug

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Bug with id {bug_id} not found",
    )


@router.patch("/{bug_id}", response_model=BugResponse)
def update_bug(bug_id: int, bug_update: BugUpdate):
    for bug in bugs_db:
        if bug["id"] == bug_id:
            update_data = bug_update.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                bug[key] = value

            return bug

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Bug with id {bug_id} not found",
    )