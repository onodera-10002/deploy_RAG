import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# 環境変数 DATABASE_URL があればそれを使い、なければローカルの設定を使う
# (Renderにデプロイした時は Aiven の URL が使われるようになる)
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+aiomysql://user:password@db/rag_db")

# Aiven (クラウド) かどうかで設定を少し変える
connect_args = {}
if "aivencloud" in DATABASE_URL:
    # Aiven用のSSL設定 (簡易版)
    # ※本来は証明書検証が必要ですが、まずは接続優先でチェックを緩めます
    connect_args = {"ssl": {"check_hostname": False, "verify_mode": False}}

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