
import streamlit as st

st.set_page_config(
    page_title="VeltaRune",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
header, footer, [data-testid="stSidebar"] {
    display: none !important;
}

.stApp {
    background: #000;
    color: white;
}

.block-container {
    max-width: 1000px;
    padding-top: 2rem;
}

.title {
    text-align: center;
    font-family: monospace;
    font-size: clamp(42px, 8vw, 76px);
    font-weight: 900;
    color: white;
    text-shadow: 4px 4px #555;
    margin-top: 25px;
}

.scene {
    border: 3px solid white;
    padding: 30px 15px;
    text-align: center;
    font-family: monospace;
    background:
        radial-gradient(ellipse at 50% 100%,
        #333 0%, #111 35%, #000 75%);
    min-height: 300px;
}

.stButton > button {
    background: black !important;
    color: white !important;
    border: 2px solid white !important;
    border-radius: 0 !important;
    font-family: monospace !important;
    font-size: 20px !important;
    font-weight: bold !important;
    min-height: 55px;
    width: 100%;
}

.stButton > button:hover {
    color: #ff4545 !important;
    border-color: #ff4545 !important;
}
</style>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="title">✦ VeltaRune ✦</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="scene">
<br>
<pre style="color:#aaa; font-size:16px; line-height:1.15">
        .       *       .       *
    /\\                         /\\
   /  \\       /\u005c        /\\      /  \\
  /    \\_____/  \\______/  \\____/    \\

        /\\    /\u005c    /\\
_______/  \\__/  \\__/  \\___________
          |  |
          |__|
          /  \\
         /____\\
</pre>
<p style="font-size:18px;color:#aaa">
A JOURNEY BETWEEN WORLDS
</p>
<br>
</div>
""", unsafe_allow_html=True)

st.write("")

left, center, right = st.columns([1, 2, 1])

with center:
    if st.button("♥   NEW GAME", use_container_width=True):
        st.session_state["page"] = "game"

    if st.button("⚙   SETTINGS", use_container_width=True):
        st.session_state["page"] = "settings"

page = st.session_state.get("page", "menu")

if page == "game":
    st.markdown("---")
    st.subheader("♥  VeltaRune")
    st.write("Cuộc hành trình của bạn bắt đầu...")
    if st.button("← BACK TO MENU"):
        st.session_state["page"] = "menu"
        st.rerun()

elif page == "settings":
    st.markdown("---")
    st.subheader("SETTINGS")
    volume = st.slider("Âm lượng", 0, 100, 70)
    fullscreen = st.checkbox("Chế độ toàn màn hình")
    if st.button("← BACK TO MENU"):
        st.session_state["page"] = "menu"
        st.rerun()
