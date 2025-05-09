from typing import Annotated

from fastapi import Depends

from todo_api.core.database.dependencies import AsyncDbSession
from todo_api.todos.service import TodoService as TodoService_


def get_todo_service(session: AsyncDbSession) -> TodoService_:
    return TodoService_(session)


TodoService = Annotated[TodoService_, Depends(get_todo_service)]
