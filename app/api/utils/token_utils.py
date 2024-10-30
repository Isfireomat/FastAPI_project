from datetime import datetime, timezone, timedelta
from fastapi import Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from app.api.db_utils.db_crud import get_user
from app.api.db_utils.db_connect import get_session
from typing import Optional, Dict, Any

SECRET_KEY = "This_is_your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

redirect_to_login = lambda: RedirectResponse(url="/login")

async def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode: Dict[str, Any] = data.copy()
    to_encode.update({"exp": datetime.utcnow() + (expires_delta or timedelta(minutes=15))})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(request: Request, session: AsyncSession = Depends(get_session)) -> Optional[Any]:
    token: Optional[str] = request.cookies.get("access_token")
    if not token:
        return redirect_to_login()

    token = token.split(" ")[1] if " " in token else token
    try:
        payload: Dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: Optional[str] = payload.get("sub")
        exp: datetime = datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc)
        if not exp or user_email is None or exp < datetime.now(timezone.utc):
            return redirect_to_login()
    except JWTError:
        return redirect_to_login()

    user: Optional[Any] = await get_user(session, user_email=user_email)
    if user is None:
        return redirect_to_login()

    return user