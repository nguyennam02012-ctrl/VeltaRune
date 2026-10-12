import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="VeltaRune — Hang của Roser", page_icon="🌹", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""<style>
#MainMenu, footer, header, [data-testid="stToolbar"], [data-testid="stDecoration"] {visibility:hidden;}
.block-container {padding:0 !important; max-width:100% !important;}
[data-testid="stAppViewContainer"] {background:#090914;}
[data-testid="stVerticalBlock"] {gap:0 !important;}
</style>""", unsafe_allow_html=True)

GAME = r'''<!doctype html><html><head><meta charset="utf-8"><style>
*{box-sizing:border-box}html,body{margin:0;width:100%;height:100%;overflow:hidden;background:#090914;color:#fff;font-family:monospace}
#wrap{width:100vw;height:100vh;min-height:520px;position:relative;background:#090914;overflow:hidden}
canvas{display:block;width:100%;height:100%;image-rendering:pixelated;outline:none}
#hud{position:absolute;left:18px;top:16px;padding:10px 14px;background:#080812dd;border:2px solid #d8c9ff;box-shadow:4px 4px 0 #34294e;line-height:1.6;font-size:14px;pointer-events:none}
#hint{position:absolute;right:18px;top:16px;padding:10px 14px;background:#080812dd;border:2px solid #d8c9ff;font-size:13px;line-height:1.6;text-align:right;pointer-events:none}
#dialog{display:none;position:absolute;left:50%;bottom:26px;transform:translateX(-50%);width:min(850px,calc(100% - 36px));min-height:110px;background:#080812f5;border:3px solid #fff;padding:18px 22px;font-size:18px;line-height:1.55;box-shadow:0 0 0 4px #27213a;}
#dialog small{display:block;text-align:right;color:#ffb2d3;margin-top:8px;font-size:13px}
#start{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;background:#090914;z-index:4}
#start .card{text-align:center;padding:36px;border:3px solid #e2d7ff;background:#11101d;box-shadow:8px 8px 0 #3d3158;max-width:560px}
#start h1{font-size:clamp(32px,5vw,58px);margin:0 0 12px;letter-spacing:3px;color:#ffd5e7}
#start p{line-height:1.7;color:#ddd5ee}
button{font: bold 16px monospace;padding:13px 28px;background:#ffb6d4;color:#1b1020;border:0;cursor:pointer;margin-top:12px}button:hover{background:#fff}
#resize{position:absolute;bottom:10px;right:14px;color:#b8abc9;font-size:11px;pointer-events:none}
</style></head><body><div id="wrap"><canvas id="game" tabindex="0"></canvas>
<div id="hud">✦ VELTARUNE<br>HANG HOA CỦA ROSER<br><span id="hp">HP ♥♥♥♥♥</span><br><span id="flowers">Hoa hồi máu: 0</span></div>
<div id="hint">WASD / ↑↓←→ : DI CHUYỂN<br>E : TƯƠNG TÁC<br>ESC : ĐÓNG HỘI THOẠI</div>
<div id="dialog">Bạn tỉnh dậy trong hang hoa của Roser.<small>Nhấn E để tiếp tục</small></div><div id="resize"></div>
<div id="start"><div class="card"><h1>✦ VeltaRune ✦</h1><p>HANG HOA CỦA ROSER<br>Một lối đi đang chờ bạn trong bóng tối.<br><br><b>WASD / phím mũi tên</b> để di chuyển · <b>E</b> để tương tác</p><button id="play">BẮT ĐẦU KHÁM PHÁ</button></div></div>
</div><script>
(()=>{
const canvas=document.getElementById('game'),ctx=canvas.getContext('2d');ctx.imageSmoothingEnabled=false;
let W=960,H=600,keys={},started=false,dialogOpen=false,dialogIndex=0,flowers=0,hp=5,exitReached=false;
const tile=32, cols=72, rows=48, worldW=cols*tile,worldH=rows*tile;
let map=Array.from({length:rows},()=>Array(cols).fill(1));
// carve winding corridors and chambers
function carve(x1,y1,x2,y2,w=3){let x=x1,y=y1;const stamp=()=>{for(let yy=y-w>>1;yy<=y+(w>>1);yy++)for(let xx=x-(w>>1);xx<=x+(w>>1);xx++)if(yy>0&&xx>0&&yy<rows-1&&xx<cols-1)map[yy][xx]=0};stamp();while(x!==x2||y!==y2){if(x!==x2&&(y===y2||Math.random()<.56))x+=Math.sign(x2-x);else y+=Math.sign(y2-y);stamp()}}
// broad cave rooms connected by corridors
function room(cx,cy,rx,ry){for(let y=cy-ry;y<=cy+ry;y++)for(let x=cx-rx;x<=cx+rx;x++)if(x>0&&y>0&&x<cols-1&&y<rows-1)map[y][x]=0}
room(7,7,6,4);room(23,8,7,5);room(42,9,8,5);room(61,8,7,5);room(12,24,8,7);room(31,24,9,6);room(53,25,9,7);room(10,41,7,4);room(32,40,9,5);room(59,41,9,4);
[[7,7,23,8],[23,8,42,9],[42,9,61,8],[7,7,12,24],[12,24,31,24],[31,24,53,25],[53,25,61,8],[12,24,10,41],[10,41,32,40],[32,40,59,41],[59,41,53,25]].forEach(a=>carve(...a,3));
// entrance and exit areas
room(7,7,6,4);room(65,41,5,4);carve(59,41,65,41,3);
const flowersPos=[{x:20,y:7},{x:39,y:9},{x:13,y:22},{x:31,y:23},{x:53,y:24},{x:10,y:40},{x:34,y:40},{x:61,y:40}].map((p,i)=>({...p,got:false,id:i}));
const chests=[{x:25,y:8,open:false},{x:32,y:40,open:false}];const roser={x:43,y:9};const exit={x:66,y:41};
const player={x:7*tile,y:7*tile,speed:190,face:'down',walk:0};
function resize(){const dpr=Math.min(devicePixelRatio||1,2);W=canvas.clientWidth;H=canvas.clientHeight;canvas.width=Math.floor(W*dpr);canvas.height=Math.floor(H*dpr);ctx.setTransform(dpr,0,0,dpr,0,0);ctx.imageSmoothingEnabled=false;document.getElementById('resize').textContent=`${Math.round(W)} × ${Math.round(H)}`}
new ResizeObserver(resize).observe(canvas);resize();
function solid(px,py){let x=Math.floor(px/tile),y=Math.floor(py/tile);return x<0||y<0||x>=cols||y>=rows||map[y][x]===1}
function move(dx,dy,dt){let nx=player.x+dx*player.speed*dt,ny=player.y+dy*player.speed*dt,r=8;if(!solid(nx-r,player.y-r)&&!solid(nx+r,player.y-r)&&!solid(nx-r,player.y+r)&&!solid(nx+r,player.y+r))player.x=nx;if(!solid(player.x-r,ny-r)&&!solid(player.x+r,ny-r)&&!solid(player.x-r,ny+r)&&!solid(player.x+r,ny+r))player.y=ny;if(dx||dy){player.walk+=dt*12;if(Math.abs(dx)>Math.abs(dy))player.face=dx>0?'right':'left';else player.face=dy>0?'down':'up'}}
function box(x,y,w,h,c){ctx.fillStyle=c;ctx.fillRect(Math.round(x),Math.round(y),w,h)}
function drawFloor(x,y,sx,sy){box(sx,sy,tile,tile,'#29233b');box(sx+2,sy+2,tile-4,tile-4,'#322a46');if((x*7+y*11)%9===0)box(sx+8,sy+18,3,3,'#4a3c59');if((x+y*3)%17===0){box(sx+6,sy+7,3,3,'#55425f');box(sx+22,sy+23,2,2,'#49384f')}}
function drawWall(x,y,sx,sy){box(sx,sy,tile,tile,'#171322');box(sx+2,sy+2,tile-4,tile-4,'#494052');box(sx+3,sy+3,tile-6,4,'#67586c');box(sx+4,sy+9,tile-8,2,'#30283d');box(sx+5,sy+14,3,3,'#74617a');box(sx+tile-8,sy+20,4,3,'#282235');if((x*13+y*7)%23===0){box(sx+6,sy+tile-5,5,3,'#5f9d83');box(sx+10,sy+tile-8,3,4,'#70bd91')}}
function flower(sx,sy){ctx.save();ctx.translate(sx+16,sy+16);ctx.fillStyle='#ff6cae';for(let i=0;i<5;i++){ctx.beginPath();ctx.ellipse(0,-6,4,6,i*Math.PI*2/5,0,Math.PI*2);ctx.fill()}ctx.fillStyle='#ffe6a1';ctx.fillRect(-2,-2,4,4);ctx.restore();box(sx+13,sy+23,6,3,'#4e9c68')}
function person(sx,sy){let bob=Math.sin(player.walk)*2;sy+=bob; // shadow
box(sx+5,sy+25,22,5,'#171321');
// legs
box(sx+9,sy+20,5,8,'#29244e');box(sx+18,sy+20,5,8,'#29244e');if(Math.sin(player.walk)>0){box(sx+7,sy+26,7,3,'#e9d7c8');box(sx+18,sy+26,7,3,'#e9d7c8')}else{box(sx+9,sy+26,7,3,'#e9d7c8');box(sx+20,sy+26,6,3,'#e9d7c8')}
// shirt with Vietnam star
box(sx+7,sy+9,18,13,'#8d2447');box(sx+4,sy+10,5,11,'#d9a17c');box(sx+23,sy+10,5,11,'#d9a17c');box(sx+10,sy+12,12,8,'#d82d3f');ctx.fillStyle='#ffe36a';ctx.beginPath();ctx.moveTo(sx+16,sy+12);ctx.lineTo(sx+17.5,sy+15);ctx.lineTo(sx+21,sy+15);ctx.lineTo(sx+18.2,sy+17);ctx.lineTo(sx+19.2,sy+20);ctx.lineTo(sx+16,sy+18);ctx.lineTo(sx+13,sy+20);ctx.lineTo(sx+14,sy+17);ctx.lineTo(sx+11,sy+15);ctx.lineTo(sx+14.5,sy+15);ctx.closePath();ctx.fill();
// head + hair
box(sx+9,sy+1,14,10,'#e8b58d');box(sx+8,sy,16,5,'#34233a');box(sx+7,sy+3,4,6,'#34233a');box(sx+21,sy+3,4,6,'#34233a');if(player.face!=='up'){box(sx+12,sy+5,2,2,'#20152a');box(sx+19,sy+5,2,2,'#20152a')}}
function monster(sx,sy){box(sx+5,sy+26,24,4,'#171321');ctx.fillStyle='#f08bb8';for(let i=0;i<6;i++){ctx.beginPath();ctx.ellipse(sx+17+Math.cos(i*Math.PI/3)*9,sy+12+Math.sin(i*Math.PI/3)*8,6,10,i*Math.PI/3,0,Math.PI*2);ctx.fill()}ctx.fillStyle='#c82e70';ctx.beginPath();ctx.arc(sx+17,sy+15,9,0,Math.PI*2);ctx.fill();box(sx+11,sy+12,4,4,'#fff4fa');box(sx+20,sy+12,4,4,'#fff4fa');box(sx+12,sy+13,2,3,'#302039');box(sx+21,sy+13,2,3,'#302039');box(sx+13,sy+19,9,2,'#7e174a')}
function chest(sx,sy,open){box(sx+4,sy+11,25,17,'#7b472e');box(sx+4,sy+10,25,6,open?'#b38b58':'#e0a653');box(sx+7,sy+15,19,10,'#a96a39');box(sx+15,sy+16,4,6,'#ffe28a');if(open){box(sx+3,sy+6,27,5,'#c89c63')}}
function render(){ctx.clearRect(0,0,W,H);let scale=Math.min(W/960,H/600); // fill screen, preserve pixels
const viewW=W/scale,viewH=H/scale;let camX=Math.max(0,Math.min(worldW-viewW,player.x-viewW/2));let camY=Math.max(0,Math.min(worldH-viewH,player.y-viewH/2));
ctx.save();ctx.scale(scale,scale);ctx.translate(-camX,-camY);
let minX=Math.max(0,Math.floor(camX/tile)-1),maxX=Math.min(cols-1,Math.ceil((camX+viewW)/tile)+1),minY=Math.max(0,Math.floor(camY/tile)-1),maxY=Math.min(rows-1,Math.ceil((camY+viewH)/tile)+1);
for(let y=minY;y<=maxY;y++)for(let x=minX;x<=maxX;x++){let sx=x*tile,sy=y*tile;if(map[y][x]===1)drawWall(x,y,sx,sy);else drawFloor(x,y,sx,sy)}
// decorative crystals and pools
for(let y=minY;y<=maxY;y++)for(let x=minX;x<=maxX;x++)if(map[y][x]===0&&(x*17+y*31)%137===0){box(x*tile+12,y*tile+10,5,10,'#75e0ce');box(x*tile+10,y*tile+18,9,3,'#397d83')}
flowersPos.forEach(f=>{if(!f.got)flower(f.x*tile,f.y*tile)});chests.forEach(c=>chest(c.x*tile,c.y*tile,c.open));monster(roser.x*tile,roser.y*tile);
// exit gate
box(exit.x*tile+3,exit.y*tile-3,26,35,'#a58bc9');box(exit.x*tile+7,exit.y*tile+2,18,27,'#171221');box(exit.x*tile+12,exit.y*tile+8,8,8,'#ffe6a3');
person(player.x-16,player.y-16);
// vignette and ambient lights
ctx.restore();let grad=ctx.createRadialGradient(W/2,H/2,Math.min(W,H)*.15,W/2,H/2,Math.max(W,H)*.72);grad.addColorStop(0,'#08061200');grad.addColorStop(1,'#05040dcc');ctx.fillStyle=grad;ctx.fillRect(0,0,W,H);
// update hud
 document.getElementById('hp').textContent='HP '+'♥'.repeat(hp)+'♡'.repeat(5-hp);document.getElementById('flowers').textContent='Hoa hồi máu: '+flowers;
}
const dialog=document.getElementById('dialog');const lines=[];function say(text){dialog.innerHTML=text+'<small>Nhấn E để tiếp tục</small>';dialog.style.display='block';dialogOpen=true}
function interact(){if(dialogOpen){dialog.style.display='none';dialogOpen=false;return}let tx=Math.round(player.x/tile),ty=Math.round(player.y/tile);let near=(x,y)=>Math.hypot(tx-x,ty-y)<2.2;let f=flowersPos.find(f=>!f.got&&near(f.x,f.y));if(f){f.got=true;flowers++;hp=Math.min(5,hp+1);say('Bạn hái được một <span style="color:#ff8fc0">bông hoa hồi máu</span>. Cánh hoa ấm lên trong tay bạn.');return}let c=chests.find(c=>!c.open&&near(c.x,c.y));if(c){c.open=true;say('Trong rương có một <span style="color:#ffe08a">Cổ Ấn Velta</span>. Nó khẽ phát sáng...');return}if(near(roser.x,roser.y)){say('RO SER: “Ồ? Có người lạc vào khu vườn của ta à? Nếu muốn ra ngoài, hãy đi về phía đông nam. Nhưng đừng để bóng tối đánh lừa nhé.”');return}if(near(exit.x,exit.y)){say('Cánh cửa đá rung lên. Cổ Ấn Velta có thể mở nó...');return}say('Hang động im lặng. Những cánh hoa phát sáng mờ mờ trong bóng tối.')}
function keydown(e){let k=e.key.toLowerCase();if(['arrowup','arrowdown','arrowleft','arrowright',' '].includes(k))e.preventDefault();keys[k]=true;if(k==='e'&&started)interact();if(k==='escape'&&dialogOpen){dialogOpen=false;dialog.style.display='none'}}function keyup(e){keys[e.key.toLowerCase()]=false}window.addEventListener('keydown',keydown);window.addEventListener('keyup',keyup);window.addEventListener('blur',()=>keys={});
document.getElementById('play').onclick=()=>{started=true;document.getElementById('start').style.display='none';canvas.focus()};
let last=performance.now();function loop(now){let dt=Math.min((now-last)/1000,.04);last=now;if(started&&!dialogOpen){let dx=(keys.d||keys.arrowright?1:0)-(keys.a||keys.arrowleft?1:0),dy=(keys.s||keys.arrowdown?1:0)-(keys.w||keys.arrowup?1:0);if(dx&&dy){dx*=.7071;dy*=.7071}move(dx,dy,dt);if(Math.hypot(player.x-exit.x*tile,player.y-exit.y*tile)<25&&!exitReached){exitReached=true;say('Bạn đã tìm thấy lối ra khỏi hang hoa của Roser! Hành trình VeltaRune mới chỉ bắt đầu...')}}render();requestAnimationFrame(loop)}requestAnimationFrame(loop);
})();
</script></body></html>'''

components.html(GAME, height=900, scrolling=False)
