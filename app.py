
import streamlit as st

st.set_page_config(
    page_title="VeltaRune",
    page_icon="🎮"
)

st.title("🎮 VeltaRune")
st.write("Chào mừng đến với thế giới game của tôi!")

if st.button("Bắt đầu"):
    st.success("Game đang hoạt động!")

