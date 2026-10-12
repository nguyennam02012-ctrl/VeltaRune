import streamlit as st
import random

st.set_page_config(page_title="VeltaRune — Hang của Roser", page_icon="🌹", layout="centered")

st.markdown("""
<style>
[data-testid="stHeader"],[data-testid="stToolbar"],[data-testid="stSidebar"]{display:none}
.stApp { background:#07070c; color:#f4f0ff; }
.block-container { max-width:850px; padding-top:1rem; padding-bottom:2rem; }
h1,h2,h3,p,label { color:#f4f0ff !important; }
div.stButton > button {
  width:100%; min-height:42px; border-radius:0;
  background:#090910; color:#f7f3ff; border:2px solid #c9c2e8;
  font-family:monospace; font-weight:bold;
}
div.stButton > button:hover { color:#ff8fc5; border-color:#ff8fc5; background:#211020; }
.cave-frame {
  border:3px solid #d6d0ee; background:#050509; padding:12px;
  font-family:monospace; white-space:pre; line-height:1.25;
  font-size:16px; overflow-x:auto; color:#a8a1c9;
}
.story {border:2px solid #c9c2e8; padding:12px; font-family:monospace; background:#08080f;}
.small {font-size:12px;color:#b9b2d7}
</style>
""", unsafe_allow_html=True)

W, H = 19, 13
WALL, FLOOR, FLOWER, EXIT, PLAYER, CHEST = "#", ".", "f", "E", "@", "C"

ROOM = [
"###################",
"##....#.......f..E#",
"##....#...........#",
"##....####.########",
"##.................#",
"####.#######.#######",
"#....#.....#.......#",
"#....#..f..#.......#",
"#.......C..........#",
"####.##########.####",
"#..............f...#",
"#.@...............##",
"###################",
]
# Normalize rows to a consistent width for safe movement/rendering.
ROOM = [row[:W].ljust(W, "#") for row in ROOM]
MAP_H, MAP_W = len(ROOM), len(ROOM[0])

def fresh_game():
    st.session_state.map = [list(r) for r in ROOM]
    st.session_state.px, st.session_state.py = 2, 11
    st.session_state.hp = 20
    st.session_state.flowers = 0
    st.session_state.chest_open = False
    st.session_state.message = "Bạn tỉnh dậy trong hang hoa của ROSER. Tìm lối ra ở phía đông!"
    st.session_state.steps = 0
    st.session_state.won = False

def tile(x, y):
    if x < 0 or y < 0 or x >= MAP_W or y >= MAP_H:
        return WALL
    return st.session_state.map[y][x]

def move(dx, dy):
    if st.session_state.won:
        return
    nx, ny = st.session_state.px + dx, st.session_state.py + dy
    target = tile(nx, ny)
    if target == WALL:
        st.session_state.message = "Bạn chạm vào vách đá lạnh. Lối này bị chặn."
        return
    st.session_state.steps += 1
    st.session_state.px, st.session_state.py = nx, ny
    if target == FLOWER:
        st.session_state.flowers += 1
        st.session_state.hp = min(20, st.session_state.hp + 2)
        st.session_state.map[ny][nx] = FLOOR
        st.session_state.message = "Bạn nhặt được một cánh hoa hồng lấp lánh. +2 HP!"
    elif target == CHEST:
        st.session_state.map[ny][nx] = FLOOR
        st.session_state.chest_open = True
        st.session_state.hp = 20
        st.session_state.message = "Bạn mở chiếc rương cũ và tìm thấy Bánh Mì Việt Nam. HP đã hồi đầy!"
    elif target == EXIT:
        st.session_state.won = True
        st.session_state.message = "Bạn tìm thấy cửa hang! ROSER thì thầm: “Chúng ta sẽ còn gặp lại...”"
    else:
        # Gentle cave hazards: occasionally a rose thorn nicks the player.
        if random.random() < 0.12:
            st.session_state.hp = max(0, st.session_state.hp - 1)
            st.session_state.message = "Một chiếc gai nhỏ quẹt qua áo bạn. -1 HP."
        else:
            st.session_state.message = random.choice([
                "Tiếng nước nhỏ giọt vang vọng trong hang...",
                "Những cánh hoa hồng phát sáng trên vách đá.",
                "Bạn nghe thấy tiếng ROSER hát rất khẽ ở sâu trong hang.",
                "Một làn gió mát thổi từ phía lối ra."
            ])
    if st.session_state.hp <= 0:
        st.session_state.message = "Bạn kiệt sức trong hang. Hãy bắt đầu lại."
        st.session_state.won = False
        st.session_state.dead = True

def draw_map():
    rows = []
    for y, row in enumerate(st.session_state.map):
        chars = []
        for x, cell in enumerate(row):
            if (x, y) == (st.session_state.px, st.session_state.py):
                chars.append("🧍")
            elif cell == WALL:
                chars.append("🪨")
            elif cell == FLOWER:
                chars.append("🌸")
            elif cell == EXIT:
                chars.append("🚪")
            elif cell == CHEST:
                chars.append("📦")
            else:
                chars.append("　")
        rows.append("".join(chars))
    return "\n".join(rows)

if "map" not in st.session_state:
    fresh_game()
    st.session_state.dead = False

st.markdown("<h1 style='text-align:center;font-family:monospace'>✦ VeltaRune ✦</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#ff9dc9!important;font-family:monospace'>HANG HOA CỦA ROSER</p>", unsafe_allow_html=True)

if st.session_state.won:
    st.success("BẠN ĐÃ THOÁT KHỎI HANG ROSER!")
elif st.session_state.get("dead", False):
    st.error("GAME OVER — bạn đã hết HP.")

left, right = st.columns([2, 1])
with left:
    st.markdown('<div class="story">MỤC TIÊU: khám phá hang, nhặt hoa hồi máu và tìm cửa ra 🚪</div>', unsafe_allow_html=True)
    st.markdown('<div class="small">Điều khiển bằng các nút mũi tên bên dưới bản đồ. 🪨 = đá, 🌸 = hoa, 📦 = rương, 🚪 = lối ra.</div>', unsafe_allow_html=True)
    st.markdown('<div class="cave-frame">' + draw_map() + '</div>', unsafe_allow_html=True)
with right:
    st.markdown("### NHÂN VẬT")
    st.write("🧍 **Bạn**")
    st.write(f"HP: **{st.session_state.hp}/20**")
    st.progress(st.session_state.hp / 20)
    st.write(f"🌸 Hoa đã nhặt: **{st.session_state.flowers}**")
    st.write(f"👣 Bước đi: **{st.session_state.steps}**")
    st.markdown("---")
    st.markdown("### ROSER")
    st.markdown('<div style="text-align:center;font-size:30px;color:#ff8fc5">✿ ❀ 🌹 ❀ ✿</div>', unsafe_allow_html=True)
    st.caption("Cánh hoa hồng lấp lánh trong bóng tối...")

st.markdown("### DI CHUYỂN")
up1, up2, up3 = st.columns([1,1,1])
with up2:
    if st.button("⬆ ĐI LÊN", disabled=st.session_state.won or st.session_state.get("dead", False)):
        move(0,-1); st.rerun()
l1, l2, l3 = st.columns([1,1,1])
with l1:
    if st.button("⬅ SANG TRÁI", disabled=st.session_state.won or st.session_state.get("dead", False)):
        move(-1,0); st.rerun()
with l2:
    if st.button("⬇ ĐI XUỐNG", disabled=st.session_state.won or st.session_state.get("dead", False)):
        move(0,1); st.rerun()
with l3:
    if st.button("SANG PHẢI ➡", disabled=st.session_state.won or st.session_state.get("dead", False)):
        move(1,0); st.rerun()

st.markdown('<div class="story">✦ ' + st.session_state.message + '</div>', unsafe_allow_html=True)
if st.button("↻ CHƠI LẠI TỪ ĐẦU"):
    fresh_game()
    st.session_state.dead = False
    st.rerun()
