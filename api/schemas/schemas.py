from pydantic import BaseModel

# RAGのシステムに学習させるダータ
class IngestRequest(BaseModel):
    text: str # RAGに読み込ませる文章
    source: str #出典
    category: str #カテゴリ

# チャットの入出力のデータ
class ChatRequest(BaseModel):
    query: str # 質問
    session_id: str # 会話の流れを定義するid

class ChatResponse(BaseModel):
    answer: str # RAGで生成した回答




