from fastapi import FastAPI, APIRouter
from db import Database
from config import DATABASE_URL
from models import Users, BaseResponse

app = FastAPI()

router = APIRouter()
db = Database(db_url=DATABASE_URL)


@router.get('/users/', response_model=BaseResponse)
async def read_users():
    await db.connect()
    users = await db.read_users()
    await db.close()
    return BaseResponse(data=list(users))

@router.get('/users/{user_id}', response_model=BaseResponse)
async def read_user_detail(user_id: int):
    await db.connect()
    user_detail = await db.read_user_detail(user_id=user_id)
    await db.close()
    return BaseResponse(data=dict(user_detail))


@router.post('/users/', response_model=BaseResponse)
async def create_user(user: Users):
    await db.connect()
    await db.create_user(user.fullname, user.username, user.email, user.password)
    await db.close()
    return BaseResponse(data=dict(user))


@router.put('/users/{user_id}', response_model=BaseResponse)
async def update_user(user: Users, user_id: int):
    await db.connect()
    await db.update_user(user_id, user.fullname, user.username, user.email, user.password)
    await db.close()
    return BaseResponse(data=f"User with id {user_id} updated successfully")



@router.delete('/users/{user_id}', response_model=BaseResponse)
async def delete_user(user_id: int):
        await db.connect()
        await db.delete_user(user_id)
        await db.close()
        return BaseResponse(data=f"User with id {user_id} deleted successfully")


app.include_router(router, prefix="/api", tags=["Users CRUD API"])