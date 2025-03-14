from fastapi import FastAPI, APIRouter
from db import Database
from config import DATABASE_URL
from models import Users, BaseResponse

app = FastAPI()

router = APIRouter()
db = Database(db_url=DATABASE_URL)


@router.get('/users/')
async def read_users():
    try:
        await db.connect()
        users = await db.read_users()
        return BaseResponse(status=True, body=list(users), error="null")

    except Exception as e:
        return BaseResponse(status=False, body="null", error=str(e))

    finally:
        await db.close()



@router.post('/users/')
async def create_user(user : Users):
    try:
        await db.connect()
        await db.create_user(user.fullname, user.username, user.email, user.password)
        return BaseResponse(status=True, body=dict(user), error="null")

    except Exception as e:
        return BaseResponse(status=False, body="null", error=str(e))

    finally:
        await db.close()



@router.put('/users/{user_id}')
async def update_user(user: Users, user_id: int):
    try:
        await db.connect()
        await db.update_user(user_id, user.fullname, user.username, user.email, user.password)
        return BaseResponse(status=True, body=f"User with id {user_id} updated successfully", error="null")

    except Exception as e:
        return BaseResponse(status=False, body="null", error=str(e))

    finally:
        await db.close()


@router.delete('/users/{user_id}')
async def delete_user(user_id: int):
    try:
        await db.connect()
        await db.delete_user(user_id)
        return BaseResponse(status=True, body=f"User with id {user_id} deleted successfully", error="null")

    except Exception as e:
        return BaseResponse(status=False, body="null", error=str(e))

    finally:
        await db.close()


app.include_router(router, prefix="/api", tags=["Users CRUD API"])