import os
import ssl  # <--- ★追加：これが必要です
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# 環境変数 DATABASE_URL があればそれを使い、なければローカルの設定を使う
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+aiomysql://user:password@db/rag_db")

# Aiven (クラウド) かどうかで設定を変える
connect_args = {}
if "aivencloud" in DATABASE_URL:
    # ★修正ポイント：辞書ではなく、本物のSSLContextオブジェクトを作る！
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    # 辞書の中身を「ssl_contextオブジェクト」にする
    connect_args = {"ssl": ssl_context}

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    connect_args=connect_args
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()