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
from typing import Optional, Union, List, Dict
from app.api.utils.token_utils import get_current_user
from app.api.models.schemas import QueryParams, ImageResponse, approveResponse
from app.api.models.models import User, Picture
from sqlalchemy.future import select
from sqlalchemy import insert, update, delete
from fastapi.responses import RedirectResponse

router = APIRouter()
@router.post("/api/approve",response_model=Dict[str,str])
async def approve(response: Response,
                  approve: approveResponse,
                  session: AsyncSession = Depends(get_session),
                   client: Redis = Depends(get_client),
                   user: dict = Depends(get_current_user)):
    if approve:
        stmt = update(Picture).where(Picture.id==int(approve.id)).values(is_active=True)
    else:
        stmt = delete(Picture).where(Picture.id==approve.id)
    await session.execute(stmt)
    await session.commit()
    result = await session.execute(select(Picture).where(Picture.id==approve.id))
    picture = result.scalar_one_or_none()  
    return {'result':str(picture.is_active)}
    
@router.post("/api/pictures",response_model=ImageResponse)
async def pictures(response: Response,
                   query_params: QueryParams,
                   session: AsyncSession = Depends(get_session),
                   client: Redis = Depends(get_client),
                   user: dict = Depends(get_current_user)) ->List[Dict[str, Union[str, bool]]]:
    match query_params.mod:
        case "all":
            result = await session.execute(select(Picture).where(Picture.is_active==True)) 
            pictures = result.scalars().all()
            pictures_json = [
                {"src": b64encode(picture.binary_picture).decode('utf-8'), 
                 "title": picture.title, 
                 "author": picture.user.name if picture.user else "Unknown",
                 "request":False} 
                for picture in pictures
            ]
            return {"images":pictures_json}
        case "my":
            result = await session.execute(select(Picture).where(Picture.is_active==True, 
                                                                 Picture.user_id==user.id)) 
            pictures = result.scalars().all()
            pictures_json = [
                {"src": b64encode(picture.binary_picture).decode('utf-8'), 
                 "title": picture.title, 
                 "author": picture.user.name if picture.user else "Unknown",
                 "request":False} 
                for picture in pictures
            ]
            return {"images":pictures_json}
        case "request":
            if not user.is_super:
                return RedirectResponse(url="/pictures?mod=all", status_code=303)
            result = await session.execute(select(Picture).where(Picture.is_active==False)) 
            pictures = result.scalars().all()
            pictures_json = [
                {"src": b64encode(picture.binary_picture).decode('utf-8'), 
                 "title": picture.title, 
                 "author": picture.user.name,
                 "request":True,
                 "id": picture.id} 
                for picture in pictures
            ]
            return {"images":pictures_json}
    return RedirectResponse(url="/pictures?mod=all", status_code=303)


@router.post("/api/upload")
async def upload_photo(response: Response,
                       photo: UploadFile = File(...),
                       session: AsyncSession = Depends(get_session),
                       client: Redis = Depends(get_client),
                       user: dict = Depends(get_current_user)) -> dict[str, Optional[str]]:
    """
    Эндпоин загрузки фотографии

    Тут фотография сравнивается с прочими в БД или кеше 
    Возвращает результат сравнения
    """
    content: bytes = await photo.read()
    result: Optional[list[float | bytes]] = await redis_crud.get_picture_result(client, content)
    if result: 
        if round(result[0], 2) == 0:
            return {"result": f"{result[0]:.2f}"}
        return {
            "result": f"{result[0]:.2f}", 
            "picture": b64encode(result[1]).decode('utf-8')
        }
    pictures: list[bytes] = await redis_crud.get_pictures(client, "pictures")
    if not pictures:
        pictures = await db_crud.get_pictures(session)
        await redis_crud.set_pictures(client, "pictures", pictures, 20)
    if pictures:
        result = max([[compare_images(content, picture), picture] for picture in pictures], key=lambda x: x[0])
        await redis_crud.set_picture(client, content, result, 10)
        picture = await db_crud.get_picture_by_bytes(session, content)
        if not picture:
            await db_crud.create_picture(session, schemas.Picture(binary_picture=content, title=photo.filename, user_id=user.id))
        if round(result[0], 2) == 0:
            return {"result": f"{result[0]:.2f}"}  
        return {
            "result": f"{result[0]:.2f}", 
            "picture": b64encode(result[1]).decode('utf-8')
        }
    await db_crud.create_picture(session, schemas.Picture(binary_picture=content, title=photo.filename, user_id=user.id ))
    return {"result": "0"}