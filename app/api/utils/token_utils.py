import os
from datetime import datetime, timezone, timedelta
from fastapi import Depends, HTTPException, status, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from app.api.db_utils.db_crud import get_user
from app.api.db_utils.db_connect import get_session
from typing import Optional, Dict, Any

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = timedelta(minutes=2)
REFRESH_TOKEN_EXPIRE_MINUTES = timedelta(days=30)

redirect_to_login = lambda: RedirectResponse(url="/login")
async def create_refresh_token(data: Dict[str, Any], 
                               expires_delta: Optional[timedelta] = None
                               ) -> str:
    """
    Создаёт refresh токен
    """
    to_encode: Dict[str, Any] = data.copy()
    to_encode.update({"exp": datetime.utcnow() + (expires_delta or timedelta(minutes=15))})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def create_access_token(data: Dict[str, Any], 
                              expires_delta: Optional[timedelta] = None
                              ) -> str:
    """
    Создаёт access токен 
    """
    to_encode: Dict[str, Any] = data.copy()
    to_encode.update({"exp": datetime.utcnow() + (expires_delta or timedelta(minutes=15))})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(request: Request, 
                           response: Response,
                           session: AsyncSession = Depends(get_session),
                           ) -> Optional[Any]:
    """
    Возвращает пользователя по токену, либо отправляет на страницу 
    авторизации, если есть проблемы с токеном или пользователя
    не существует 
    """
    async def get_access_token_from_refresh_token(request: Request, response: Response):
        """
        Функция для получения access_token через refresh_token
        """
        refresh_token: Optional[str] = request.cookies.get("refresh_token")
        if not refresh_token:  
            return None
        refresh_token = refresh_token.split(" ")[1] if " " in refresh_token else refresh_token
        refresh_payload: Dict[str, Any] = jwt.decode(refresh_token, 
                                                        SECRET_KEY, 
                                                        algorithms=[ALGORITHM])
        refresh_user_email: Optional[str] = refresh_payload.get("sub")
        refresh_exp: datetime = datetime.fromtimestamp(refresh_payload.get("exp"),
                                                        tz=timezone.utc)
        if not refresh_exp or refresh_exp < datetime.now(timezone.utc):
            return None
        access_token = await create_access_token(data={"sub": refresh_user_email}, 
                                                        expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES)
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=int(ACCESS_TOKEN_EXPIRE_MINUTES.total_seconds())
        )
        return access_token
    
    token: Optional[str] = request.cookies.get("access_token")
    if not token:
        token = await get_access_token_from_refresh_token(request, response)
        if not token:
            return redirect_to_login()
    token = token.split(" ")[1] if " " in token else token
    try:
        payload: Dict[str, Any] = jwt.decode(token, SECRET_KEY, 
                                             algorithms=[ALGORITHM])
        user_email: Optional[str] = payload.get("sub")
        exp: datetime = datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc)
        if user_email is None: return redirect_to_login() 
        if not exp or exp < datetime.now(timezone.utc):
            token = await get_access_token_from_refresh_token(request, response)
            if not token:
                return redirect_to_login()
            payload: Dict[str, Any] = jwt.decode(token, SECRET_KEY, 
                                                 algorithms=[ALGORITHM])
            user_email: Optional[str] = payload.get("sub")
    except JWTError:
        return redirect_to_login()
    user: Optional[Any] = await get_user(session, user_email=user_email)
    if user is None:
        return redirect_to_login()
    return user