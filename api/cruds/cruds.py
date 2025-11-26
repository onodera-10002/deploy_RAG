from sqlalchemy.ext.asyncio import AsyncSession
from api.models.models import Message

async def create_message(
    db: AsyncSession,
    session_id: str,
    role: str,
    content: str
) -> Message:
    
    # データを作成する
    msg = Message(
        session_id = session_id,
        role = role,
        content = content
    )

    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg

    

