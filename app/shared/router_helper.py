from app.shared import ExceptionRaiser
from pydantic import BaseModel


class RouterMode:
    GET: str = "get"
    GET_ALL: str = "get_all"
    POST: str = "create"
    PUT: str = "update"
    DELETE: str = "delete"


async def exec(
    mode: RouterMode,
    service,
    schema: BaseModel | None,
    **kwargs,
):
    function = getattr(service, mode, None)
    if function is None or not callable(function):
        ExceptionRaiser.raise_exception(
            status_code=500,
            detail="Service doesn't support this operation",
        )

    if mode in [RouterMode.POST, RouterMode.PUT]:
        data = schema.model_dump(exclude_unset=True)
        result = await function(data=data, **kwargs)
    else:
        result = await function(**kwargs)

    if not result:
        ExceptionRaiser.raise_exception(status_code=404)

    return result
