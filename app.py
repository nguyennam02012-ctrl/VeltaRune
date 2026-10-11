from pathlib import Path
import base64
import streamlit as st

# VeltaRune — menu game Streamlit
# Đặt app.py và veltarune_background.png trong cùng thư mục/repository.

st.set_page_config(
    page_title="VeltaRune",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

BASE_DIR = Path(__file__).resolve().parent
BACKGROUND_PATH = BASE_DIR / "veltarune_background.png"

# CSS trang và menu. Không dùng JavaScript.
st.markdown(
    """
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"],
    [data-testid="stDecoration"], [data-testid="stStatusWidget"] {
        display: none !important;
    }
    [data-testid="stSidebar"] {display: none !important;}
    .stApp {
        background: #000;
        color: #fff;
    }
    .block-container {
        max-width: 1000px;
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    h1, h2, h3, p, label {
        color: #fff !important;
    }

    /* Khung chứa ảnh nền và các nút phủ trực tiếp lên ảnh */
    .st-key-game_menu {
        position: relative;
        width: 100%;
    }
    .st-key-game_menu [data-testid="stImage"] {
        width: 100%;
        margin: 0 !important;
        line-height: 0;
    }
    .st-key-game_menu [data-testid="stImage"] img {
        display: block;
        width: 100%;
        height: auto;
        image-rendering: pixelated;
        border: 2px solid #f5f5f5;
        box-sizing: border-box;
    }

    /* Streamlit đặt các nút sau ảnh; đưa chúng lên vùng menu ở giữa ảnh */
    .st-key-game_menu [data-testid="stButton"] {
        position: absolute;
        left: 50%;
        transform: translateX(-50%);
        width: min(46%, 360px);
        z-index: 10;
        margin: 0 !important;
    }
    .st-key-game_menu .st-key-new_game {
        position: absolute;
        left: 50%;
        top: 67%;
        transform: translateX(-50%);
        width: min(46%, 360px);
        z-index: 10;
        margin: 0 !important;
    }
    .st-key-game_menu .st-key-settings {
        position: absolute;
        left: 50%;
        top: 78%;
        transform: translateX(-50%);
        width: min(46%, 360px);
        z-index: 10;
        margin: 0 !important;
    }
    .st-key-game_menu [data-testid="stButton"] button {
        width: 100%;
        min-height: 44px;
        background: rgba(0, 0, 0, 0.88) !important;
        color: white !important;
        border: 2px solid white !important;
        border-radius: 0 !important;
        font-family: monospace !important;
        font-weight: bold !important;
        letter-spacing: 1px;
        box-shadow: 3px 3px 0 #777;
    }
    .st-key-game_menu [data-testid="stButton"] button:hover {
        background: #242038 !important;
        border-color: #ff4d65 !important;
        color: #ff4d65 !important;
    }
    .st-key-game_menu [data-testid="stButton"] button:focus {
        box-shadow: 0 0 0 2px #ff4d65 !important;
    }

    .game-panel {
        border: 2px solid white;
        padding: 1.25rem;
        margin-top: 1rem;
        background: #080808;
        font-family: monospace;
    }
    .game-panel p {font-family: monospace;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    "<h1 style='text-align:center;font-family:monospace;letter-spacing:3px;"
    "text-shadow:3px 3px #555;margin:0.1rem 0 0.7rem;'>✦ VeltaRune ✦</h1>",
    unsafe_allow_html=True,
)

if not BACKGROUND_PATH.is_file():
    st.error(
        "Không tìm thấy ảnh nền `veltarune_background.png`. "
        "Hãy tải ảnh này lên GitHub, đặt cùng thư mục với `app.py`."
    )
    st.stop()

# Ảnh nền và nút được đặt trong cùng container để CSS phủ nút lên ảnh.
with st.container(key="game_menu"):
    st.image(str(BACKGROUND_PATH), use_container_width=True)
    # Hai nút này được phủ lên ảnh bằng CSS phía trên.
    new_game = st.button("♥  NEW GAME", key="new_game", use_container_width=True)
    settings = st.button("⚙  SETTINGS", key="settings", use_container_width=True)

if new_game:
    st.session_state["screen"] = "game"
if settings:
    st.session_state["screen"] = "settings"

screen = st.session_state.get("screen", "menu")

if screen == "game":
    st.markdown(
        """
        <div class="game-panel">
        <h2>♥ VELTARUNE</h2>
        <p>Chuyến hành trình của bạn bắt đầu...</p>
        <p>Màn chơi hiện đang là bản khởi đầu. Bạn có thể thêm cốt truyện,
        nhân vật và hệ thống chiến đấu vào phần này.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("← BACK TO MENU", key="back_game"):
        st.session_state["screen"] = "menu"
        st.rerun()

elif screen == "settings":
    st.markdown('<div class="game-panel">', unsafe_allow_html=True)
    st.subheader("⚙ SETTINGS")
    st.write("Tùy chỉnh trải nghiệm chơi.")
    st.session_state["music_enabled"] = st.checkbox(
        "Bật nhạc nền", value=st.session_state.get("music_enabled", True)
    )
    st.session_state["fullscreen_hint"] = st.checkbox(
        "Hiệu ứng pixel", value=st.session_state.get("fullscreen_hint", True)
    )
    st.markdown("</div>", unsafe_allow_html=True)
    if st.button("← BACK TO MENU", key="back_settings"):
        st.session_state["screen"] = "menu"
        st.rerun()
