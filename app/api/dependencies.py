from typing import Annotated, AsyncGenerator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import ValidationError

from app.core.config import settings
from app.database.mongodb import get_database_session
from app.core.errors import AuthenticationError
from app.schemas.auth import TokenPayload, UserInDB

# OAuth2 password bearer scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

# Database dependency
async def get_db() -> AsyncGenerator:
    async with get_database_session() as db:
        yield db


# Authentication dependencies
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncGenerator, Depends(get_db)]
) -> UserInDB:
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET, 
            algorithms=[settings.JWT_ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise AuthenticationError("Token expirado")
            
        # Get user from database
        user_collection = db["usuarios"]
        user = await user_collection.find_one({"_id": token_data.sub})
        
        if not user:
            raise AuthenticationError("Usuário não encontrado")
            
        return UserInDB(**user)
        
    except (JWTError, ValidationError):
        raise AuthenticationError("Credenciais inválidas")


# Optional current user dependency
async def get_optional_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncGenerator = Depends(get_db)
) -> Optional[UserInDB]:
    try:
        return await get_current_user(token, db)
    except AuthenticationError:
        return None
        

# Admin user dependency
async def get_admin_user(
    current_user: Annotated[UserInDB, Depends(get_current_user)]
) -> UserInDB:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissões de administrador necessárias"
        )
    return current_user