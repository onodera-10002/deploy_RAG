import streamlit as st
import requests
import uuid

# バックエンドのURL (ローカル開発用)
API_URL = "http://app:8000"  # Docker内通信用

st.title("AIチャット")

# 1. セッションIDの管理 (ブラウザリロード対策)
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# 2. メッセージ履歴の管理
if "messages" not in st.session_state:
    st.session_state.messages = []

# 3. 過去のメッセージを表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. 入力フォームと送信処理
if prompt := st.chat_input("質問を入力してください..."):
    # ユーザーの入力を表示
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # APIに送信
    with st.chat_message("assistant"):
        try:
            response = requests.post(
                f"{API_URL}/chat",
                json={
                    "query": prompt,
                    "session_id": st.session_state.session_id
                }
            )
            
            if response.status_code == 200:
                answer = response.json()["answer"]
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.error(f"エラーが発生しました: {response.status_code}")
        
        except Exception as e:
            st.error(f"通信エラー: {e}")

# サイドバー：学習機能
with st.sidebar:
    st.header("📚 知識を登録")
    ingest_text = st.text_area("覚えさせたい文章")
    ingest_source = st.text_input("出典 (例: 社内規定)")
    
    if st.button("学習させる"):
        if ingest_text and ingest_source:
            res = requests.post(
                f"{API_URL}/ingest",
                json={
                    "text": ingest_text,
                    "source": ingest_source,
                    "category": "manual"
                }
            )
            if res.status_code == 200:
                st.success("覚えました！")
            else:
                st.error("学習失敗")