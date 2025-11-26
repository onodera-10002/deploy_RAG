import os
import google.generativeai as genai
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from qdrant_client import QdrantClient
from qdrant_client.http import models
import uuid

from api.db import get_db
from api.schemas.schemas import ChatRequest, IngestRequest, ChatResponse
import api.cruds.cruds as message_crud


# 基本設定
# APIキーも環境変数から取るように戻します
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Qdrantの設定を環境変数対応にする
QDRANT_URL = os.getenv("QDRANT_URL", "http://qdrant:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None) # ローカルではNoneでOK

genai.configure(api_key=GOOGLE_API_KEY)

# APIキーを渡して接続するように変更！
qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

router = APIRouter()

@router.post("/ingest")
async def ingest_data(req: IngestRequest):
    
    embedding = genai.embed_content(
        model="models/text-embedding-004",
        content=req.text
    )
    vector = embedding["embedding"]

    point_id = str(uuid.uuid4())
    qdrant.upsert(
        collection_name="documents",
        points=[
            models.PointStruct(
                id=point_id,
                vector=vector,
                # ★ここで決めたキー名(text, source)が「正」となる
                payload={
                    "text": req.text,
                    "source": req.source,
                    "category": req.category
                }
            )
        ]
    )
    return {"message": "Data ingested successfully", "point_id": point_id}


# 質問を読み取り、回答を作成するエンドポイント
@router.post("/chat", response_model = ChatResponse)
async def chat(req: ChatRequest, db: AsyncSession = Depends(get_db)):
    """
    RAGの処理:検索して、dbに質問文と回答を保存する
    """
    print(f"質問受信:{req.query}")

    #　質問の保存
    await message_crud.create_message(db=db, session_id=req.session_id, role="user", content=req.query)

    # 質問のベクトル化
    query_embedding = genai.embed_content(
        model="gemini-embeddings-001",
        content=req.query
    )
    query_vector = query_embedding["embedding"]

    search_results = qdrant.search(
        collection_name="documents",
        query_vector=query_vector,
        limit=3
    )
    context_text = ""
    for hit in search_results:
        text = hit.payload["text"]
        source = hit.payload["source"]
        context_text += f"- {text} (出典: {source})\n"

    # Geminiへの命令文を作成
    prompt = f"""
    あなたは親切なアシスタントです。以下の「参考情報」だけを使って、ユーザーの質問に答えてください。
    もし情報がない場合は「わかりません」と答えてください。嘘をつかないでください。
    [参考情報]
    {context_text}
    [ユーザーの質問]
    {req.query}
    """
    model = genai.GenarativeModel("gemini-2.5-flash")
    response = model.generate_content(prompt)
    ai_answer = response.text

    await message_crud.createmessage(
        db = db,
        session_id = req.session_id,
        role = "assistant",
        content = ai_answer
    )

    return ChatResponse(answer = ai_answer)
    
    

    
    


