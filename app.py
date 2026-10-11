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
    st.image("veltarune_title.png", use_container_width=True)

    left, center, right = st.columns([1, 1.2, 1])

    with center:
        if st.button("♥  NEW GAME", use_container_width=True):
            st.session_state.screen = "new_game"
            st.rerun()

        if st.button("⚙  SETTINGS", use_container_width=True):
            st.session_state.screen = "settings"
            st.rerun()

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
