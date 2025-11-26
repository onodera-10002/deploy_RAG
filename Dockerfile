FROM python:3.11-slim

WORKDIR /app

# mysqlclient を削除し、代わりに pymysql を入れます
# これなら C言語のコンパイラが不要なので、エラーが出ません
RUN pip install fastapi uvicorn sqlalchemy aiomysql pymysql pydantic qdrant-client==1.9.0 cryptography google-generativeai


COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]