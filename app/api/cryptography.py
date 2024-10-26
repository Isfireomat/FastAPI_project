
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status, Request
from app.api.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import RedirectResponse
from app.api.CRUD import get_user
from datetime import datetime, timezone


SECRET_KEY = "This_is_your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
redirect_to_login = lambda:RedirectResponse(url="/login")

async def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + (expires_delta or timedelta(minutes=15))})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(request: Request, db: AsyncSession = Depends(get_db)):
    token = request.cookies.get("access_token")

    if not token: return redirect_to_login()
    
    token = token.split(" ")[1] if " " in token else token

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email: str = payload.get("sub")
        exp = datetime.fromtimestamp(payload.get("exp"), tz=timezone.utc) 
        if not exp: redirect_to_login()
        if user_email is None or exp < datetime.utcnow(): return redirect_to_login()
    except JWTError:
        return redirect_to_login()
    
    user = await get_user(db, user_email=user_email)
    if user is None:    return redirect_to_login()
    
    return user