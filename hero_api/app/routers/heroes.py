from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.db import get_session
from app.dependencies import get_current_admin, get_current_user
from app.models import Hero, HeroCreate, HeroResponse, HeroUpdate, Mission, User

router = APIRouter(prefix="/heroes", tags=["Heroes"])


@router.post("/", response_model=HeroResponse, status_code=status.HTTP_201_CREATED)
def create_hero(
    hero_data: HeroCreate,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    hero = Hero(**hero_data.model_dump())
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@router.get("/", response_model=list[HeroResponse])
def list_heroes(session: Session = Depends(get_session)):
    return session.exec(select(Hero)).all()


@router.get("/{hero_id}", response_model=HeroResponse)
def get_hero(hero_id: int, session: Session = Depends(get_session)):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@router.patch("/{hero_id}", response_model=HeroResponse)
def update_hero(
    hero_id: int,
    patch: HeroUpdate,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_user),
):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    for key, value in patch.model_dump(exclude_unset=True).items():
        setattr(hero, key, value)

    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


@router.delete("/{hero_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_hero(
    hero_id: int,
    session: Session = Depends(get_session),
    _: User = Depends(get_current_admin),
):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")

    active_missions = session.exec(
        select(Mission).where(Mission.hero_id == hero_id, Mission.completed == False)
    ).first()
    if active_missions:
        raise HTTPException(status_code=400, detail="Hero has active missions")

    session.delete(hero)
    session.commit()
