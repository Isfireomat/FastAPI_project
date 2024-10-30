from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi import File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from app.api.utils.picture_utils import compare_images
from app.api.db_utils.db_connect import get_session
from app.api.redis_utils.redis_connect import get_client

from app.api.redis_utils import redis_crud
from app.api.db_utils import db_crud

from app.api.models import schemas
from base64 import b64encode

router = APIRouter()

@router.post("/api/upload")
async def upload_photo(response: Response, photo: UploadFile = File(...),
                       session: AsyncSession = Depends(get_session),
                       client: Redis = Depends(get_client)):
    content = await photo.read()
    result = await redis_crud.get_picture_result(client, content)
    if result: 
        if round(result[0],2)==0: return {"result": f"{result[0]:.2f}"}
        return {"result": f"{result[0]:.2f}", 
                "picture": b64encode(result[1]).decode('utf-8')} 
    pictures = await redis_crud.get_pictures(client, "pictures")
    if not pictures:
        pictures = await db_crud.get_pictures(session)
        await redis_crud.set_pictures(client, "pictures", pictures, 20)
    if pictures:
        result = max([[compare_images(content, picture),picture] for picture in pictures],
                     key=lambda x: x[0])
        redis_crud.set_picture(client, content, result, 10)
        picture = await db_crud.get_picture_by_bytes(session, content)
        if not picture: await db_crud.create_picture(session, 
                                             schemas.Picture(binary_picture=content))
        if round(result[0],2)==0: return {"result": f"{result[0]:.2f}"}
        return {"result": f"{result[0]:.2f}", 
                "picture": b64encode(result[1]).decode('utf-8')}
    await db_crud.create_picture(session, schemas.Picture(binary_picture=content))
    return {"result": "0"}
