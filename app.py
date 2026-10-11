import base64
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="VeltaRune", page_icon="❤️", layout="wide")

st.markdown("""
<style>
  .stApp { background: #000; color: #fff; }
  #MainMenu, footer, header, [data-testid="stSidebar"] { visibility: hidden; }
  .block-container { max-width: 1200px; padding: 0.5rem 0.5rem 2rem; }
  div.stButton > button {
    background: #000; color: #fff; border: 2px solid #fff;
    border-radius: 0; font-family: monospace; font-weight: bold;
  }
  div.stButton > button:hover { color: #ff3333; border-color: #ff3333; }
</style>
""", unsafe_allow_html=True)

# Screen is stored in the URL so the clickable areas in the image can
# navigate back to the Streamlit app without an extra component package.
screen = st.query_params.get("screen", "title")

if screen == "title":
    image_path = Path(__file__).parent / "veltarune_title.png"
    if not image_path.exists():
        st.error("Không tìm thấy veltarune_title.png. Hãy tải cả hai file trong project lên cùng thư mục GitHub.")
        st.stop()

    image_b64 = base64.b64encode(image_path.read_bytes()).decode("ascii")
    components.html(
        f"""
        <div id="menu">
          <img id="art" src="data:image/png;base64,{image_b64}" alt="VeltaRune game menu">
          <!-- Transparent click zones are aligned over the menu text in the artwork. -->
          <button class="hit new-game" aria-label="New Game" title="New Game"
            onclick="go('new_game')"></button>
          <button class="hit settings" aria-label="Settings" title="Settings"
            onclick="go('settings')"></button>
        </div>
        <style>
          html, body { margin:0; padding:0; background:#000; overflow:hidden; }
          #menu { position:relative; width:100%; line-height:0; }
          #art { display:block; width:100%; height:auto; }
          .hit {
            position:absolute; left:37.5%; width:25%; height:7.2%;
            border:2px solid transparent; background:transparent; padding:0;
            cursor:pointer; box-sizing:border-box;
          }
          .hit:hover, .hit:focus-visible {
            outline:2px solid #fff; background:rgba(255,255,255,.10);
          }
          .new-game { top:42.5%; }
          .settings { top:50.2%; }
        </style>
        <script>
          function go(screen) {
            const target = window.parent.location.origin + window.parent.location.pathname
                         + '?screen=' + encodeURIComponent(screen);
            window.parent.location.href = target;
          }
        </script>
        """,
        height=600,
        scrolling=False,
    )
    st.caption("Bấm trực tiếp vào NEW GAME hoặc SETTINGS trong khung menu của ảnh.")

elif screen == "new_game":
    st.markdown("<h1 style='text-align:center;color:white;font-family:monospace'>VELTARUNE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;font-family:monospace'>YOUR JOURNEY BEGINS HERE...</p>", unsafe_allow_html=True)
    st.divider()
    st.write("Đây là màn hình mở đầu mẫu. Bạn có thể thêm cốt truyện và gameplay ở đây.")
    if st.button("← BACK TO MENU"):
        st.query_params.clear()
        st.rerun()

elif screen == "settings":
    st.markdown("<h1 style='text-align:center;color:white;font-family:monospace'>SETTINGS</h1>", unsafe_allow_html=True)
    st.slider("Âm lượng", 0, 100, 70)
    st.selectbox("Giao diện", ["Pixel Classic", "Dark"])
    if st.button("← BACK TO MENU"):
        st.query_params.clear()
        st.rerun()

else:
    st.query_params.clear()
    st.rerun()
