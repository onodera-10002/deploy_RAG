FROM python:3.11-slim

WORKDIR /app

# mysqlclient を削除し、代わりに pymysql を入れます
# これなら C言語のコンパイラが不要なので、エラーが出ません
RUN pip install fastapi uvicorn sqlalchemy aiomysql pymysql pydantic qdrant-client==1.9.0 cryptography google-generativeai


COPY . .

# 環境変数 PORT があればそれを使い、なければ 8000 を使う設定
# ※ ["..."] の書き方ではなく、直接書くのがポイントです（変数を展開するため）
CMD uvicorn api.main:app --host 0.0.0.0 --port ${PORT:-8000}