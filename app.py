
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="VeltaRune",
    page_icon="❤️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background: black;
    color: white;
}
.block-container {
    max-width: 1100px;
    padding-top: 1rem;
}
div.stButton > button {
    background: black;
    color: white;
    border: 2px solid white;
    border-radius: 0;
    font-family: monospace;
    font-size: 20px;
    min-height: 48px;
}
div.stButton > button:hover {
    color: red;
    border-color: red;
}
</style>
""", unsafe_allow_html=True)

if "screen" not in st.session_state:
    st.session_state.screen = "title"

if st.session_state.screen == "title":
    image_path = Path(__file__).parent / "VeltaRune_ New Game at Dusk.png"

    if image_path.exists():
        st.image(str(image_path), use_container_width=True)
    else:
        st.title("VeltaRune")
        st.warning("Hãy kiểm tra lại tên file ảnh trong GitHub.")

    left, center, right = st.columns([1, 1.2, 1])

    with center:
        if st.button("♥ NEW GAME", use_container_width=True):
            st.session_state.screen = "new_game"
            st.rerun()

        if st.button("⚙ SETTINGS", use_container_width=True):
            st.session_state.screen = "settings"
            st.rerun()

elif st.session_state.screen == "new_game":
    st.title("VeltaRune")
    st.write("Your journey begins here...")

    if st.button("BACK"):
        st.session_state.screen = "title"
        st.rerun()

elif st.session_state.screen == "settings":
    st.title("SETTINGS")
    st.slider("Âm lượng", 0, 100, 70)

    if st.button("BACK"):
        st.session_state.screen = "title"
        st.rerun()
