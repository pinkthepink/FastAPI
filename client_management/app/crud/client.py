from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientUpdate


class CRUDClient(CRUDBase[Client, ClientCreate, ClientUpdate]):
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[Client]:
        query = select(Client).where(Client.email == email)
        result = await db.execute(query)
        return result.scalars().first()
    
    async def get_multi_by_owner(
        self, db: AsyncSession, *, owner_id: int, skip: int = 0, limit: int = 100
    ) -> List[Client]:
        query = select(Client).where(Client.created_by == owner_id).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()


client = CRUDClient(Client)