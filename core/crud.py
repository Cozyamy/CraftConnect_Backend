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
    arg: str,
    db: Session,
    model: type,
    op: str = "==",
) -> Any:

    # define valid operations in db
    operations = {
        "==": getattr(model, arg) == param,
        "!=": getattr(model, arg) != param,
        ">": getattr(model, arg) > param,
        "<": getattr(model, arg) < param,
        ">=": getattr(model, arg) >= param,
        "<=": getattr(model, arg) <= param,
    }

    # check if the operator is valid
    if op not in operations:
        raise ValueError(f"Invalid operator: {op}")

    # construct the query
    query = select(model).where(operations[op])

    # return value from db
    return db.exec(statement=query).first()
