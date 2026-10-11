
import streamlit as st

st.set_page_config(
    page_title="VeltaRune",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ẩn giao diện mặc định của Streamlit
st.markdown("""
<style>
    #MainMenu, footer, header,
    [data-testid="stSidebar"],
    [data-testid="stHeader"] {
        visibility: hidden;
        display: none;
    }

    .stApp {
        background: #000000;
        color: white;
    }

    .block-container {
        padding: 1rem 1rem 2rem 1rem;
        max-width: 1100px;
    }

    div.stButton > button {
        background: #000000;
        color: white;
        border: 2px solid white;
        border-radius: 0;
        font-family: monospace;
        font-size: 22px;
        font-weight: bold;
        min-height: 55px;
        width: 100%;
    }

    div.stButton > button:hover {
        color: #ff3333;
        border-color: #ff3333;
        background: #111111;
    }

    .caption {
        color: #888888;
        text-align: center;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# Trạng thái màn hình
if "screen" not in st.session_state:
    st.session_state.screen = "title"

if st.session_state.screen == "title":

    # Ảnh màn hình chờ đã tải lên cùng app.py
  
import streamlit as st
import streamlit.components.v1 as components
import base64
from pathlib import Path

image_path = Path(__file__).parent / "veltarune_title.png"

if image_path.exists():
    image_data = base64.b64encode(image_path.read_bytes()).decode()

    components.html(
        f"""
        <div id="game-menu">
          <img src="data:image/png;base64,{image_data}" />

          <button class="game-button new-game"
            onclick="window.parent.postMessage(
              {{type: 'streamlit:setComponentValue',
               value: 'new_game'}}, '*')">
            ♥ NEW GAME
          </button>

          <button class="game-button settings"
            onclick="window.parent.postMessage(
              {{type: 'streamlit:setComponentValue',
               value: 'settings'}}, '*')">
            ⚙ SETTINGS
          </button>
        </div>

        <style>
          #game-menu {
            position: relative;
            width: 100%;
            line-height: 0;
          }

          #game-menu img {
            display: block;
            width: 100%;
            height: auto;
          }

          .game-button {
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            width: 24%;
            height: 7%;
            background: transparent;
            color: white;
            border: none;
            font-family: monospace;
            font-size: clamp(10px, 1.5vw, 20px);
            font-weight: bold;
            cursor: pointer;
            line-height: normal;
          }

          .game-button:hover {
            color: #ff3333;
            background: rgba(255,255,255,0.08);
          }

          .new-game { top: 43%; }
          .settings { top: 51%; }
        </style>
        """,
        height=650,
        scrolling=False,
    )
else:
    st.error("Không tìm thấy file veltarune_title.png")


elif st.session_state.screen == "new_game":
    st.title("NEW GAME")
    st.write("Your journey begins here...")
    st.info("Màn chơi đầu tiên sẽ được phát triển tại đây.")

    if st.button("BACK"):
        st.session_state.screen = "title"
        st.rerun()

elif st.session_state.screen == "settings":
    st.title("SETTINGS")

    volume = st.slider("Âm lượng", 0, 100, 70)
    fullscreen_style = st.selectbox(
        "Giao diện",
        ["Pixel Classic", "Dark"]
    )

    st.write(f"Âm lượng: {volume}%")
    st.write(f"Giao diện: {fullscreen_style}")

    if st.button("BACK"):
        st.session_state.screen = "title"
        st.rerun()
