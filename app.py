import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="VeltaRune — Hang của Roser", page_icon="🌹", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""<style>
html,body,[data-testid="stAppViewContainer"],[data-testid="stHeader"]{background:#080810!important;color:#f5f0ff!important}
[data-testid="stMainBlockContainer"]{padding:0!important;max-width:100%!important}
[data-testid="stToolbar"],footer,#MainMenu{visibility:hidden}
</style>""", unsafe_allow_html=True)

GAME = r'''<!DOCTYPE html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box}html,body{margin:0;background:#080810;color:#f8f2ff;font-family:monospace;overflow:hidden}#wrap{width:100%;height:100vh;min-height:650px;display:flex;flex-direction:column;align-items:center;background:radial-gradient(ellipse at 50% 45%,#21142d 0,#0a0912 70%)}
#top{height:64px;display:flex;align-items:center;justify-content:space-between;width:min(1100px,98vw);padding:8px 16px}#logo{font-size:26px;letter-spacing:3px;font-weight:bold;color:#fff;text-shadow:3px 3px #7e3c8e}#stats{font-size:13px;color:#f2c5ef;text-align:right;line-height:1.8}#screen{position:relative;width:min(1100px,98vw);height:calc(100vh - 154px);min-height:490px;border:4px solid #bda9d9;box-shadow:0 0 0 4px #20172d,0 0 35px #7a347455;overflow:hidden;background:#100d1a}canvas{width:100%;height:100%;display:block;image-rendering:pixelated}#hint{height:86px;width:min(1100px,98vw);display:flex;align-items:center;justify-content:space-between;gap:12px;padding:10px 16px;color:#d8c9ed;font-size:13px}#dialog{position:absolute;left:3%;right:3%;bottom:3%;min-height:100px;border:4px solid #fff;background:#080810;box-shadow:0 0 0 4px #17111e;padding:14px 18px;font-size:17px;line-height:1.55;display:none;white-space:pre-wrap}#dialog b{color:#ff85bc;display:block;margin-bottom:5px}#prompt{position:absolute;top:12px;left:14px;padding:7px 10px;background:#080810dd;border:2px solid #6f587f;color:#e7d6f3;font-size:12px}kbd{border:1px solid #ad91c6;padding:3px 6px;background:#1c1426;color:white;border-radius:3px}
@media(max-width:600px){#logo{font-size:18px}#stats{font-size:10px}#hint{font-size:11px}#dialog{font-size:14px}}
</style></head><body><div id="wrap"><div id="top"><div id="logo">✦ VELTARUNE ✦</div><div id="stats">HP <span id="hp">20</span>/20　✿ <span id="flowers">0</span><br><span id="status">HANG HOA CỦA ROSER</span></div></div><div id="screen"><canvas id="game" width="960" height="600"></canvas><div id="prompt">WASD / ↑↓←→ DI CHUYỂN　·　E TƯƠNG TÁC</div><div id="dialog"><b id="speaker">ROSE​R</b><span id="words"></span><div style="text-align:right;font-size:12px;color:#c7b4d8;margin-top:8px">[ ENTER / E để tiếp tục ]</div></div></div><div id="hint"><span>✦ Bạn tỉnh dậy trong hang hoa của Roser. Tìm lối ra phía đông!</span><span><kbd>WASD</kbd> Di chuyển　<kbd>E</kbd> Tương tác</span></div></div>
<script>
const c=document.getElementById('game'),ctx=c.getContext('2d');ctx.imageSmoothingEnabled=false;
const TILE=40, world={w:24,h:15};
// 1 = wall, 0 = floor
const map=[
'111111111111111111111111','100000000000000000000001','101111110111111101111101','100000010000000001000001','111110011111011101011101','100010000000010001000001','101011111011110111011101','100000000010000000000001','101111011110111111011101','100001000000000001000001','101101111011111101110101','100000000010000000000001','101111011110111111011101','100000000000000000000001','111111111111111111111111'];
let px=100,py=500,hp=20,flowers=0,chestOpen=false,exitOpen=false,dialogue=null,dialogIndex=0,keys={},last=0,stepSound=0;
const flowerSpots=[{x:300,y:180,got:false},{x:580,y:420,got:false},{x:740,y:260,got:false},{x:460,y:500,got:false}];
const chest={x:300,y:380};const roser={x:820,y:180};const exit={x:875,y:535};
function wallAt(x,y){let tx=Math.floor(x/TILE),ty=Math.floor(y/TILE);if(tx<0||ty<0||tx>=world.w||ty>=world.h)return true;return map[ty][tx]==='1'}
function collides(x,y){let r=10;return wallAt(x-r,y-r)||wallAt(x+r,y-r)||wallAt(x-r,y+r)||wallAt(x+r,y+r)}
function rect(x,y,w,h,col){ctx.fillStyle=col;ctx.fillRect(Math.round(x),Math.round(y),w,h)}
function text(t,x,y,size,col='#fff'){ctx.font=`${size}px monospace`;ctx.fillStyle=col;ctx.fillText(t,x,y)}
function drawFlower(x,y,scale=1){let s=scale;for(let i=0;i<5;i++){let a=i*Math.PI*2/5;rect(x+Math.cos(a)*7*s-4*s,y+Math.sin(a)*7*s-4*s,8*s,8*s,'#f46aab');rect(x+Math.cos(a)*7*s-2*s,y+Math.sin(a)*7*s-2*s,4*s,4*s,'#ffb5d8')}rect(x-3*s,y-3*s,6*s,6*s,'#ffe28a')}
function drawHuman(x,y){ // pixel sprite with Vietnam-star shirt
rect(x-8,y+8,16,9,'#382348');rect(x-8,y-7,16,16,'#e8d6bd');rect(x-10,y-13,20,8,'#342238');rect(x-7,y-18,14,7,'#342238');rect(x-12,y+1,6,12,'#d9bda9');rect(x+6,y+1,6,12,'#d9bda9');rect(x-7,y+9,5,10,'#4b4d9a');rect(x+2,y+9,5,10,'#4b4d9a');rect(x-5,y-3,10,8,'#df273e'); // flag shirt
// yellow star
ctx.fillStyle='#ffe45e';ctx.beginPath();for(let i=0;i<10;i++){let a=-Math.PI/2+i*Math.PI/5,r=i%2?2:4;let xx=x+Math.cos(a)*r,yy=y+1+Math.sin(a)*r;i?ctx.lineTo(xx,yy):ctx.moveTo(xx,yy)}ctx.closePath();ctx.fill();rect(x-5,y-8,3,2,'#201528');rect(x+3,y-8,3,2,'#201528')}
function drawRoser(x,y){ // flower monster
for(let i=0;i<8;i++){let a=i*Math.PI/4;rect(x+Math.cos(a)*17-7,y+Math.sin(a)*17-7,14,14,i%2?'#c93475':'#ff75b2')}rect(x-11,y-11,22,22,'#ee4d91');rect(x-7,y-4,4,5,'#211127');rect(x+4,y-4,4,5,'#211127');rect(x-4,y+5,8,2,'#5d193f');rect(x-4,y+18,3,9,'#3e925b');rect(x+2,y+18,3,9,'#3e925b')}
function drawChest(x,y){rect(x-13,y-9,26,20,'#9b562e');rect(x-13,y-9,26,7,chestOpen?'#c18a4a':'#d99a4d');rect(x-2,y-3,5,6,'#ffe58c');rect(x-12,y+9,24,3,'#563047');if(chestOpen){rect(x-9,y-15,18,5,'#d4a65b')}}
function draw(){ctx.clearRect(0,0,960,600);rect(0,0,960,600,'#151020');
// tiled cave floor
for(let y=0;y<world.h;y++)for(let x=0;x<world.w;x++){let wall=map[y][x]==='1';let xx=x*TILE,yy=y*TILE;if(wall){rect(xx,yy,40,40,'#443454');rect(xx+3,yy+3,34,34,'#665174');rect(xx+5,yy+5,30,5,'#8d739b');rect(xx+5,yy+12,5,17,'#382a49');rect(xx+12,yy+27,22,4,'#493754');if((x+y)%3===0)rect(xx+24,yy+16,5,5,'#a18aae')}else{rect(xx,yy,40,40,'#21192d');if((x*7+y*3)%5===0)rect(xx+8,yy+8,3,3,'#30223c');if((x+y)%7===0)rect(xx+27,yy+29,2,2,'#55405e')}}
// glowing moss
for(let i=0;i<24;i++){let x=(i*137+43)%930+10,y=(i*79+30)%560+15;if(!wallAt(x,y)){rect(x,y,3,3,'#6bba9b');rect(x-3,y-3,9,9,'#5cc69b22')}}
flowerSpots.forEach(f=>{if(!f.got){drawFlower(f.x,f.y,.8);}});drawChest(chest.x,chest.y);drawRoser(roser.x,roser.y);
// exit rune
rect(exit.x-14,exit.y-18,28,36,exitOpen?'#4bd6ad':'#463054');rect(exit.x-9,exit.y-13,18,26,exitOpen?'#a6ffe3':'#8a5e9d');text(exitOpen?'↗':'✦',exit.x-7,exit.y+5,16,exitOpen?'#102a25':'#ffe8a8');
// player glow
ctx.fillStyle='#ffdc8a22';ctx.beginPath();ctx.arc(px,py,30,0,Math.PI*2);ctx.fill();drawHuman(px,py);
// nearby prompt
let near=Math.hypot(px-roser.x,py-roser.y)<58||Math.hypot(px-chest.x,py-chest.y)<48||flowerSpots.some(f=>!f.got&&Math.hypot(px-f.x,py-f.y)<40)||Math.hypot(px-exit.x,py-exit.y)<50;
document.getElementById('prompt').style.borderColor=near?'#ff85bc':'#6f587f';
}
function say(speaker,lines){dialogue={speaker,lines};dialogIndex=0;showLine();document.getElementById('dialog').style.display='block'}function showLine(){document.getElementById('speaker').textContent=dialogue.speaker;document.getElementById('words').textContent=dialogue.lines[dialogIndex]}
function interact(){if(dialogue){dialogIndex++;if(dialogIndex>=dialogue.lines.length){dialogue=null;document.getElementById('dialog').style.display='none'}else showLine();return}
if(Math.hypot(px-roser.x,py-roser.y)<60){say('ROSER',['Ồ… cuối cùng cậu cũng tỉnh rồi.','Những cánh hoa ở đây giữ lại chút sinh lực. Đừng để bóng tối nuốt mất cậu.','Cánh cửa phía đông chỉ mở khi cậu tìm được cổ ấn.']);return}
if(Math.hypot(px-chest.x,py-chest.y)<48){if(!chestOpen){chestOpen=true;exitOpen=true;say('HỆ THỐNG',['Bạn mở chiếc rương cũ.','Bên trong là Cổ Ấn phát sáng! Lối ra đã mở.'])}else say('HỆ THỐNG',['Chiếc rương trống rỗng.']);return}
let f=flowerSpots.find(f=>!f.got&&Math.hypot(px-f.x,py-f.y)<40);if(f){f.got=true;flowers++;hp=Math.min(20,hp+3);document.getElementById('hp').textContent=hp;document.getElementById('flowers').textContent=flowers;say('HỆ THỐNG',['Bạn hái được một Hoa Hồi Sinh.','HP +3. Những cánh hoa khẽ phát sáng trong tay bạn.']);return}
if(Math.hypot(px-exit.x,py-exit.y)<50){if(exitOpen){say('VELTARUNE',['Ánh sáng tràn qua cánh cửa…','CHƯƠNG 1 — HANG HOA CỦA ROSER: HOÀN THÀNH!'])}else say('HỆ THỐNG',['Cánh cửa bị khóa. Có lẽ chiếc rương kia chứa thứ mình cần.']);return}}
function update(t){let dt=Math.min((t-last)/1000||0,.035);last=t;if(!dialogue){let dx=0,dy=0;if(keys.w||keys.ArrowUp)dy--;if(keys.s||keys.ArrowDown)dy++;if(keys.a||keys.ArrowLeft)dx--;if(keys.d||keys.ArrowRight)dx++;if(dx&&dy){dx*=.7071;dy*=.7071}let speed=190;let nx=px+dx*speed*dt,ny=py+dy*speed*dt;if(!collides(nx,py))px=nx;if(!collides(px,ny))py=ny;}draw();requestAnimationFrame(update)}
addEventListener('keydown',e=>{let k=e.key.length===1?e.key.toLowerCase():e.key;if(['w','a','s','d','ArrowUp','ArrowDown','ArrowLeft','ArrowRight',' ','Enter'].includes(k))e.preventDefault();keys[k]=true;if((k==='e'||k==='Enter')&&!e.repeat)interact()});addEventListener('keyup',e=>{let k=e.key.length===1?e.key.toLowerCase():e.key;keys[k]=false});c.addEventListener('pointerdown',()=>c.focus());say('VELTARUNE',['Bạn tỉnh dậy trong hang hoa của Roser.','Dùng WASD hoặc phím mũi tên để đi. Đến gần vật thể rồi nhấn E.']);requestAnimationFrame(update);
</script></body></html>'''

components.html(GAME, height=790, scrolling=False)
