from fastapi import APIRouter

router = APIRouter()


@router.get("/hello", description="Returns a simple greeting")
async def say_hello():
    return {"message": "Hello from Omni2"}
