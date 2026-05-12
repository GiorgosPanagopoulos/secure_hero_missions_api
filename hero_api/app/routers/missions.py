from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db import get_session
from app.dependencies import get_current_admin, get_current_user
from app.models import Hero, Mission, MissionCreate, MissionResponse, MissionUpdate, User

router = APIRouter(prefix="/missions", tags=["Missions"])


@router.post("/", response_model=MissionResponse, status_code=status.HTTP_201_CREATED)
def create_mission(
    mission_data: MissionCreate,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    hero = session.get(Hero, mission_data.hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    mission = Mission(**mission_data.model_dump())
    session.add(mission)
    session.commit()
    session.refresh(mission)
    return mission


@router.get("/", response_model=list[MissionResponse])
def list_missions(session: Session = Depends(get_session)):
    return session.exec(select(Mission)).all()


@router.get("/{mission_id}", response_model=MissionResponse)
def get_mission(mission_id: int, session: Session = Depends(get_session)):
    mission = session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission


@router.patch("/{mission_id}", response_model=MissionResponse)
def update_mission(
    mission_id: int,
    patch: MissionUpdate,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    mission = session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    updates = patch.model_dump(exclude_unset=True)

    if "hero_id" in updates:
        hero = session.get(Hero, updates["hero_id"])
        if not hero:
            raise HTTPException(status_code=404, detail="Hero not found")

    for key, value in updates.items():
        setattr(mission, key, value)

    session.add(mission)
    session.commit()
    session.refresh(mission)
    return mission


@router.delete("/{mission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mission(
    mission_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_admin),
):
    mission = session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    session.delete(mission)
    session.commit()
