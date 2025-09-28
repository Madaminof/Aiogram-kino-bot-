from sqlalchemy.future import select
from model.db import async_session
from model.model import Kino

async def add_kino(code: str, name: str, message_id: int, file_id: str = None):
    async with async_session() as session:
        kino = Kino(code=code, name=name, message_id=message_id, file_id=file_id)
        session.add(kino)
        await session.commit()

async def get_kino(code: str):
    async with async_session() as session:
        result = await session.execute(select(Kino).where(Kino.code == code))
        kino = result.scalar_one_or_none()
        if kino:
            return {
                "code": kino.code,
                "name": kino.name,
                "message_id": kino.message_id,
                "file_id": kino.file_id
            }
        return None
