from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi import File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.db_connect import get_session
from app.api.db_crud import create_picture, get_picture_by_bytes, get_pictures
from app.api.utils.picture_utils import compare_images
from app.api import schemas
from base64 import b64encode

router = APIRouter()

@router.post("/api/upload")
async def upload_photo(response: Response, photo: UploadFile = File(...),
                       session: AsyncSession = Depends(get_session)):
    content = await photo.read()
    pictures = await get_pictures(session)
    if pictures:
        result = max([[compare_images(content, picture),picture] for picture in pictures],
                     key=lambda x: x[0])
        picture = await get_picture_by_bytes(session, content)
        if not picture: await create_picture(session, 
                                             schemas.Picture(binary_picture=content))
        if round(result[0],2)==0: return {"result": f"{result[0]:.2f}"}
        return {"result": f"{result[0]:.2f}", 
                "picture": b64encode(result[1]).decode('utf-8')}
    await create_picture(session, schemas.Picture(binary_picture=content))
    return {"result": "0"}
