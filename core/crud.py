from typing import Any

from sqlmodel import Session, select


async def exists_in_db(
    param: Any,
    arg: str,
    model: type,
    db: Session,
) -> bool:
    return bool(
        db.exec(statement=select(model).where(getattr(model, arg) == param)).first()
    )


async def create(
    param: dict | Any,
    table: type,
    db: Session,
) -> Any:
    # init db variable
    created = table(**param)

    # add to database
    db.add(created)
    db.commit()
    db.refresh(created)

    # return created item in db
    return created


async def get_all(model: type, db: Session) -> Any:
    return db.exec(statement=select(model)).all()


async def get_by_param(
    param: str | int | Any,
    db: Session,
    model: type,
) -> Any:
    return db.exec()
