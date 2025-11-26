import os
import asyncio
from fastapi import FastAPI
from qdrant_client import QdrantClient
from qdrant_client.http import models

# 作った部品たちをインポート
from api.routers import routers as chat
from api.db import engine, Base
# ★重要: これをインポートしないとテーブルが作られない！
from api.models import models

app = FastAPI()

app.include_router(chat.router)

QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333")
qdrant = QdrantClient(url=QDRANT_URL)

@app.on_event("startup")
async def startup():
    for i in range(15):
        try:
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            break
        except Exception as e:
            await asyncio.sleep(2)

    try:
        qdrant.create_collection(
            collection_name = "documents",
            vectors_config = models.VectorParams(size = 768, distance = models.Distance.COSINE)
        )
    except:
        pass





