import streamlit as st
from bot_engine import BotEngine

st.set_page_config(page_title="Cortex", page_icon="🧠")

# راست‌چین کردن متن فارسی
st.markdown(
    """
    <style>
    .stChatMessage, .stMarkdown { direction: rtl; text-align: right; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🧠 کورتکس")
st.caption("مشاور هوشمند شما")

# Streamlit با هر پیام کل فایل را از اول اجرا می‌کند،
# پس چیزهایی که باید بمانند را در session_state نگه می‌داریم.
if "engine" not in st.session_state:
    st.session_state.engine = BotEngine()
if "messages" not in st.session_state:
    st.session_state.messages = []

# نمایش تاریخچه
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# گرفتن ورودی جدید
user_input = st.chat_input("سوالت را بنویس...")

if user_input and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("در حال فکر کردن..."):
            try:
                reply = st.session_state.engine.generate_response(user_input)
            except Exception:
                reply = "در حال حاضر در دسترس نیستم، لطفاً کمی بعد دوباره تلاش کنید."
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

# دکمه شروع مکالمه جدید
if st.sidebar.button("مکالمه جدید"):
    st.session_state.engine = BotEngine()
    st.session_state.messages = []
    st.rerun()
