FROM python:3.11-slim

WORKDIR /app

# 必要なライブラリをインストール
RUN pip install streamlit requests

# ファイルをコピー
COPY . .

# Streamlitを起動 (ポート8501を開ける)
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]