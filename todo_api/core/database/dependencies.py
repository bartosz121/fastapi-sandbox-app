from typing import Annotated, Any, Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from todo_api.core.database.base import session_factory


def get_session() -> Generator[Session, Any, None]:
    with session_factory() as session:
        try:
            yield session
        except:
            session.rollback()
            raise
        else:
            session.commit()


DbSession = Annotated[Session, Depends(get_session)]

__all__ = (
    "get_session",
    "DbSession",
)
