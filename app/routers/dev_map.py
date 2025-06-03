from fastapi import APIRouter, Path
from typing import Union

devRouter = APIRouter()

@devRouter.get("/items/query")
async def read_query_param(q: Union[str, None] = None):
    return {"q": q}

@devRouter.get("/items/{item_id}")
async def read_path_param(item_id: int = Path(..., gt=0)):
    return {"item_id": item_id}

@devRouter.get("/items/details/{item_id}")
async def read_path_and_query(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@devRouter.delete("/items_del/{item_id}")
async def delete_by_id(item_id: int):
    return {"resultado": f"Se eliminó el item con ID {item_id}"}
