import json, sys, html as htmlmod
from pathlib import Path
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(r"D:\Harness\zyy")
OUT = ROOT / "graphify-out"
LIB = Path(r"C:\Users\zy130\AppData\Local\Temp\graphify-zyy\3d-force-graph.min.js")

graph = json.loads((OUT / "graph.json").read_text(encoding="utf-8"))
lib_js = LIB.read_text(encoding="utf-8")

raw_nodes = graph["nodes"]
raw_links = graph["links"]

# ---- degree ----
deg = Counter()
for e in raw_links:
    deg[e["source"]] += 1
    deg[e["target"]] += 1

# ---- community palette ----
comm_names = []
for n in raw_nodes:
    cn = n.get("community_name") or "未分组"
    if cn not in comm_names:
        comm_names.append(cn)
comm_names.sort()

PALETTE = [
    "#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F",
    "#EDC948", "#B07AA1", "#FF9DA7", "#9C755F", "#BAB0AC",
    "#6A5ACD", "#00CED1", "#FF6B6B", "#48C774", "#FFA07A",
    "#8E44AD", "#16A085", "#E67E22", "#2C3E50", "#D35400",
]
comm_color = {c: PALETTE[i % len(PALETTE)] for i, c in enumerate(comm_names)}

# ---- lean node payload ----
nodes = []
for n in raw_nodes:
    nodes.append({
        "id": n["id"],
        "label": n.get("label") or n["id"],
        "comm": n.get("community_name") or "未分组",
        "deg": deg.get(n["id"], 0),
        "ftype": n.get("file_type") or "concept",
        "rationale": (n.get("rationale") or "")[:220],
    })

links = []
for e in raw_links:
    links.append({
        "source": e["source"],
        "target": e["target"],
        "relation": e.get("relation", ""),
        "confidence": e.get("confidence", ""),
        "score": e.get("confidence_score", 1.0),
    })

comm_counts = Counter(n["comm"] for n in nodes)
payload = {
    "nodes": nodes,
    "links": links,
    "communities": [{"name": c, "color": comm_color[c], "count": comm_counts[c]} for c in comm_names],
}

data_js = json.dumps(payload, ensure_ascii=False).replace("<", "\\u003c")
color_js = json.dumps(comm_color, ensure_ascii=False)

TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>云计算运维知识图谱 · 3D</title>
<style>
  * { box-sizing: border-box; }
  html, body { margin:0; padding:0; height:100%; overflow:hidden;
    color:#e8ecf5; background-color:#05070d;
    /* 深空径向渐变：中心暗蓝紫 → 外围近黑 */
    background-image: radial-gradient(115% 92% at 50% 42%,
        #121a33 0%, #101832 18%, #0a0f1f 54%, #05070d 100%);
    background-repeat:no-repeat; background-attachment:fixed;
    font-family: "Segoe UI","Microsoft YaHei","PingFang SC",system-ui,sans-serif; }
  /* 星场层在 WebGL 之下；WebGL 画布透明后可透出渐变与星点 */
  #stars { position:absolute; inset:0; z-index:1; pointer-events:none; }
  #gl { position:absolute; inset:0; z-index:2; }
  .panel { position:absolute; z-index:10; background:rgba(14,19,32,.82); border:1px solid rgba(120,150,220,.22);
    border-radius:12px; backdrop-filter:blur(10px); box-shadow:0 8px 32px rgba(0,0,0,.45); }
  #title { top:16px; left:16px; padding:14px 18px; max-width:330px; }
  #title h1 { margin:0 0 6px; font-size:16px; font-weight:600; letter-spacing:.3px; }
  #title .sub { font-size:12px; color:#8fa3c8; line-height:1.6; }
  #title .stat { margin-top:8px; font-size:12px; color:#b9c8e4; }
  #title .stat b { color:#6fb3ff; font-weight:600; }
  #ctrl { top:16px; right:16px; padding:12px; width:250px; }
  #ctrl input[type=text] { width:100%; padding:8px 10px; border-radius:8px;
    border:1px solid rgba(120,150,220,.3); background:rgba(8,12,22,.85); color:#e8ecf5;
    font-size:13px; outline:none; font-family:inherit; }
  #ctrl input[type=text]:focus { border-color:#4d8cff; }
  .row { display:flex; gap:8px; margin-top:10px; flex-wrap:wrap; }
  .btn { flex:1; min-width:70px; padding:7px 9px; border-radius:8px; cursor:pointer;
    border:1px solid rgba(120,150,220,.3); background:rgba(30,42,68,.7); color:#cfe0ff;
    font-size:12px; transition:.15s; font-family:inherit; text-align:center; }
  .btn:hover { background:rgba(52,74,120,.85); border-color:#4d8cff; }
  .btn.on { background:rgba(45,110,220,.85); border-color:#6fb3ff; color:#fff; }
  #hint { bottom:16px; left:16px; padding:10px 14px; font-size:11.5px; color:#8fa3c8; line-height:1.7; }
  #hint kbd { background:rgba(120,150,220,.18); border:1px solid rgba(120,150,220,.3);
    border-radius:4px; padding:1px 5px; font-size:10.5px; }
  #legend { bottom:16px; right:16px; padding:12px; width:250px; max-height:52vh; overflow-y:auto; }
  #legend h2 { margin:0 0 8px; font-size:12px; color:#8fa3c8; font-weight:600;
    text-transform:uppercase; letter-spacing:.6px; }
  .lg { display:flex; align-items:center; gap:8px; padding:5px 7px; border-radius:7px;
    cursor:pointer; font-size:12.5px; transition:.12s; user-select:none; }
  .lg:hover { background:rgba(120,150,220,.14); }
  .lg.off { opacity:.32; }
  .lg .dot { width:10px; height:10px; border-radius:50%; flex-shrink:0; }
  .lg .nm { flex:1; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
  .lg .ct { color:#7d8fb3; font-size:11px; font-variant-numeric:tabular-nums; }
  #legend::-webkit-scrollbar { width:6px; }
  #legend::-webkit-scrollbar-thumb { background:rgba(120,150,220,.3); border-radius:3px; }
  #tip { position:absolute; pointer-events:none; padding:9px 12px; border-radius:9px;
    background:rgba(10,15,26,.95); border:1px solid rgba(120,150,220,.35); font-size:12.5px;
    max-width:300px; display:none; z-index:99; box-shadow:0 6px 24px rgba(0,0,0,.6); }
  #tip .t { font-weight:600; margin-bottom:4px; font-size:13.5px; }
  #tip .m { color:#8fa3c8; font-size:11.5px; line-height:1.6; }
  #tip .r { margin-top:5px; padding-top:5px; border-top:1px solid rgba(120,150,220,.2);
    color:#a8b8d8; font-size:11.5px; line-height:1.5; }
  #labels { position:absolute; inset:0; pointer-events:none; overflow:hidden; display:none; z-index:6; }  #labels .lb { position:absolute; transform:translate(-50%,-150%); white-space:nowrap;
    font-size:11.5px; font-weight:500; color:#e2ecff; letter-spacing:.2px;
    text-shadow:0 0 3px #000,0 0 7px #000,0 0 14px #000; }
  #loading { position:absolute; inset:0; display:flex; align-items:center; justify-content:center;
    flex-direction:column; gap:14px; background:#070a12; z-index:200; transition:opacity .5s; }
  #loading .ring { width:44px; height:44px; border:3px solid rgba(120,150,220,.2);
    border-top-color:#4d8cff; border-radius:50%; animation:spin 1s linear infinite; }
  @keyframes spin { to { transform:rotate(360deg); } }
  #loading .txt { color:#8fa3c8; font-size:13px; }
  /* the library injects its own English nav hint; we ship a Chinese one instead */
  .scene-nav-info { display:none !important; }
</style>
</head>
<body>
<canvas id="stars"></canvas>
<div id="gl"></div>

<div id="title" class="panel">
  <h1>云计算运维知识图谱 · 3D</h1>
  <div class="sub">云计算运维工程师 / SRE 方向<br>节点＝知识概念　连线＝层级与语义关联</div>
  <div class="stat">__STATS__</div>
</div>

<div id="ctrl" class="panel">
  <input type="text" id="search" placeholder="搜索知识点…（回车定位）">
  <div class="row">
    <div class="btn on" id="btn-rotate">自动旋转</div>
    <div class="btn" id="btn-label">显示名称</div>
  </div>
  <div class="row">
    <div class="btn" id="btn-reset">重置视角</div>
    <div class="btn" id="btn-all">全选社区</div>
  </div>
</div>

<div id="legend" class="panel">
  <h2>社区 / 知识域</h2>
  <div id="legend-list"></div>
</div>

<div id="hint" class="panel">
  <kbd>拖拽</kbd> 旋转　<kbd>滚轮</kbd> 缩放　<kbd>右键拖拽</kbd> 平移<br>
  <kbd>悬停</kbd> 查看详情　<kbd>单击</kbd> 高亮邻居　<kbd>双击空白</kbd> 取消
</div>

<div id="labels"></div>
<div id="tip"></div>

<div id="loading"><div class="ring"></div><div class="txt">正在构建 3D 图谱…</div></div>

<script>__LIB__</script>
<script>
const DATA = __DATA__;
const COMM_COLOR = __COLORS__;

const el = id => document.getElementById(id);
const tip = el('tip');

const nodes = DATA.nodes.map(n => Object.assign({}, n));
const links = DATA.links.map(l => Object.assign({}, l));

const activeComms = new Set(DATA.communities.map(c => c.name));
let showLabels = false;
let searchTerm = '';
let highlightSet = null;

// ---------- legend ----------
const lgList = el('legend-list');
DATA.communities
  .slice()
  .sort((a, b) => b.count - a.count)
  .forEach(c => {
    const row = document.createElement('div');
    row.className = 'lg';
    row.dataset.comm = c.name;
    row.innerHTML = '<span class="dot" style="background:' + c.color +
                    ';box-shadow:0 0 8px ' + c.color + '88"></span>' +
                    '<span class="nm"></span><span class="ct">' + c.count + '</span>';
    row.querySelector('.nm').textContent = c.name;
    row.onclick = () => {
      if (activeComms.has(c.name)) activeComms.delete(c.name); else activeComms.add(c.name);
      row.classList.toggle('off', !activeComms.has(c.name));
      refresh();
    };
    lgList.appendChild(row);
  });

// ---------- accessors ----------
function nodeVisible(n) { return activeComms.has(n.comm); }

function nodeColor(n) {
  if (highlightSet) {
    if (highlightSet.has(n.id)) return '#ffffff';
    return 'rgba(90,105,135,.16)';
  }
  if (searchTerm) {
    const hit = n.label.toLowerCase().includes(searchTerm) ||
                n.id.toLowerCase().includes(searchTerm);
    if (hit) return '#ffd93d';
    return 'rgba(90,105,135,.18)';
  }
  if (!nodeVisible(n)) return 'rgba(90,105,135,.07)';
  return COMM_COLOR[n.comm] || '#8899bb';
}

function nodeVal(n) {
  if (!nodeVisible(n) && !highlightSet && !searchTerm) return 0.4;
  return 1.6 + n.deg * 1.35;
}

function linkVisible(l) {
  const s = typeof l.source === 'object' ? l.source : null;
  const t = typeof l.target === 'object' ? l.target : null;
  if (!s || !t) return true;
  return nodeVisible(s) && nodeVisible(t);
}

function linkColor(l) {
  if (highlightSet) {
    const s = l.source.id || l.source, t = l.target.id || l.target;
    if (highlightSet.has(s) && highlightSet.has(t)) return 'rgba(255,217,61,.85)';
    return 'rgba(90,105,135,.05)';
  }
  if (!linkVisible(l)) return 'rgba(90,105,135,.03)';
  return l.relation === 'references' ? 'rgba(110,150,230,.30)' : 'rgba(230,120,180,.45)';
}

function linkWidth(l) {
  if (highlightSet) {
    const s = l.source.id || l.source, t = l.target.id || l.target;
    if (highlightSet.has(s) && highlightSet.has(t)) return 2.2;
  }
  return l.relation === 'references' ? 0.35 : 0.7;
}

// ---------- graph ----------
const Graph = ForceGraph3D({ rendererConfig: { antialias: true, alpha: true } })(el('gl'))
  .backgroundColor('rgba(0,0,0,0)')   /* 透明：透出 CSS 深空渐变与星场层 */
  .graphData({ nodes, links })
  .nodeId('id')
  .nodeLabel(n => {
    let h = '<div class="t">' + esc(n.label) + '</div>' +
            '<div class="m">' + esc(n.comm) + ' · 连接度 ' + n.deg + ' · ' + esc(n.ftype) + '</div>';
    if (n.rationale) h += '<div class="r">' + esc(n.rationale) + '</div>';
    return h;
  })
  .nodeColor(nodeColor)
  .nodeVal(nodeVal)
  .nodeOpacity(0.92)
  .nodeResolution(18)
  .linkColor(linkColor)
  .linkWidth(linkWidth)
  .linkOpacity(0.55)
  .linkDirectionalParticles(0)
  .warmupTicks(60)
  .cooldownTicks(220)
  .onNodeClick(n => focusNode(n))
  .onNodeHover(n => {
    if (n) {
      tip.style.display = 'block';
      tip.innerHTML = '<div class="t">' + esc(n.label) + '</div>' +
        '<div class="m">' + esc(n.comm) + ' · 连接度 ' + n.deg + '</div>' +
        (n.rationale ? '<div class="r">' + esc(n.rationale) + '</div>' : '');
    } else {
      tip.style.display = 'none';
    }
  })
  .onBackgroundClick(() => { highlightSet = null; refresh(); });

document.addEventListener('mousemove', e => {
  if (tip.style.display === 'block') {
    const pad = 16;
    let x = e.clientX + pad, y = e.clientY + pad;
    if (x + tip.offsetWidth > innerWidth - 8) x = e.clientX - tip.offsetWidth - pad;
    if (y + tip.offsetHeight > innerHeight - 8) y = e.clientY - tip.offsetHeight - pad;
    tip.style.left = x + 'px';
    tip.style.top = y + 'px';
  }
});

function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function refresh() {
  Graph.nodeColor(nodeColor).nodeVal(nodeVal)
       .linkColor(linkColor).linkWidth(linkWidth);
}

// ---------- focus / highlight ----------
function focusNode(n) {
  const neigh = new Set([n.id]);
  links.forEach(l => {
    const s = l.source.id || l.source, t = l.target.id || l.target;
    if (s === n.id) neigh.add(t);
    if (t === n.id) neigh.add(s);
  });
  highlightSet = neigh;
  refresh();

  const dist = 90, ratio = 1 + dist / Math.hypot(n.x || 1, n.y || 1, n.z || 1);
  Graph.cameraPosition(
    { x: (n.x || 0) * ratio, y: (n.y || 0) * ratio, z: (n.z || 0) * ratio },
    n, 900
  );
}

// ---------- controls ----------
el('btn-rotate').onclick = function () {
  this.classList.toggle('on');
  Graph.controls().autoRotate = this.classList.contains('on');
  Graph.controls().autoRotateSpeed = 0.6;
};
Graph.controls().autoRotate = true;
Graph.controls().autoRotateSpeed = 0.6;

el('btn-label').onclick = function () {
  showLabels = !showLabels;
  this.classList.toggle('on', showLabels);
  applyLabels();
};

el('btn-reset').onclick = () => {
  highlightSet = null; searchTerm = ''; el('search').value = '';
  refresh(); Graph.zoomToFit(900, 70);
};

el('btn-all').onclick = () => {
  DATA.communities.forEach(c => activeComms.add(c.name));
  document.querySelectorAll('.lg').forEach(r => r.classList.remove('off'));
  refresh();
};

el('search').addEventListener('input', function () {
  searchTerm = this.value.trim().toLowerCase();
  refresh();
});
el('search').addEventListener('keydown', function (e) {
  if (e.key === 'Enter' && searchTerm) {
    const hit = nodes.find(n => n.label.toLowerCase().includes(searchTerm) ||
                               n.id.toLowerCase().includes(searchTerm));
    if (hit) { highlightSet = null; searchTerm = ''; this.value = ''; focusNode(hit); }
  }
});

// ---------- text labels: HTML overlay projected via graph2ScreenCoords ----------
// The standalone bundle only READS window.THREE; it never sets it, so
// nodeThreeObject/Sprite is unavailable here. Projecting to screen coords and
// positioning DOM nodes needs no THREE at all.
const labelLayer = el('labels');
const labelEls = new Map();
const LABEL_MIN_DEG = __LABELMINDEG__;

// Camera forward vector is derived straight from the world matrix instead of
// calling camera.getWorldDirection(): three's Camera subclass does
// `super.getWorldDirection(target).negate()`, which chains a Vector3 method that
// a hand-rolled stand-in object does not have. Reading the matrix needs no THREE.
function cameraForward(cam) {
  if (!cam || !cam.matrixWorld) return null;
  cam.updateWorldMatrix(true, false);
  const e = cam.matrixWorld.elements;
  // Object3D.getWorldDirection() = +(e[8],e[9],e[10]); Camera negates it.
  let x = -e[8], y = -e[9], z = -e[10];
  const l = Math.hypot(x, y, z) || 1;
  return { x: x / l, y: y / l, z: z / l };
}

function applyLabels() {
  labelLayer.style.display = showLabels ? 'block' : 'none';
  if (!showLabels) labelEls.forEach(d => d.style.display = 'none');
}

function tickLabels() {
  requestAnimationFrame(tickLabels);
  if (!showLabels) return;
  try {
    const cam = Graph.camera();
    if (!cam) return;
    const fwd = cameraForward(cam);
    if (!fwd) return;
    const cp = cam.position;
    const seen = new Set();
    for (const n of nodes) {
      if (n.deg < LABEL_MIN_DEG || !nodeVisible(n)) continue;
      if (!isFinite(n.x) || !isFinite(n.y) || !isFinite(n.z)) continue;
      const dx = n.x - cp.x, dy = n.y - cp.y, dz = n.z - cp.z;
      if (dx * fwd.x + dy * fwd.y + dz * fwd.z <= 0) continue;  // behind camera
      const p = Graph.graph2ScreenCoords(n.x, n.y, n.z);
      if (!p || !isFinite(p.x) || !isFinite(p.y)) continue;
      if (p.x < -40 || p.y < -40 || p.x > innerWidth + 40 || p.y > innerHeight + 40) continue;
      seen.add(n.id);
      let d = labelEls.get(n.id);
      if (!d) {
        d = document.createElement('div');
        d.className = 'lb';
        labelLayer.appendChild(d);
        labelEls.set(n.id, d);
      }
      if (d.textContent !== n.label) d.textContent = n.label;
      d.style.left = p.x + 'px';
      d.style.top = p.y + 'px';
      d.style.display = 'block';
    }
    for (const [id, d] of labelEls) if (!seen.has(id)) d.style.display = 'none';
    delete labelLayer.dataset.err;
  } catch (e) {
    // keep the rAF loop alive and make the failure visible instead of silent
    labelLayer.dataset.err = 'ERR: ' + (e && e.message ? e.message : String(e));
  }
}
requestAnimationFrame(tickLabels);

// allow deep-linking straight into label mode: graph-3d.html?labels=1
if (new URLSearchParams(location.search).get('labels') === '1') {
  showLabels = true;
  el('btn-label').classList.add('on');
  applyLabels();
}

// ---------- 深空星场 ----------
// 注意：本页的 window.THREE 是 undefined —— 打包版内部是
//   `window.THREE ? window.THREE : {…内置实现…}`
// 它只“读”window.THREE、从不给它赋值，且 Points / PointsMaterial 无法从
// 场景图反推（场景里只有 Mesh 系对象）。所以这里不碰 window.THREE，改用
// 独立 2D 画布 + 相机 matrixWorldInverse 做透视投影，视差是真实的 3D。
//
// 密度：相机 FOV 50°，全球面只有一小部分落在视野内，所以星数要按视野
// 反推，不能按球面总数拍脑袋。STAR_N 是唯一的密度旋钮。
const STAR_N     = 6000;
const STAR_R_MIN = 1800;
const STAR_R_MAX = 3200;
const STAR_BUCKETS = 8;

const starPos   = new Float32Array(STAR_N * 3);
const starAlpha = new Float32Array(STAR_N);
const starSize  = new Float32Array(STAR_N);
const starPhase = new Float32Array(STAR_N);
const starTwk   = new Uint8Array(STAR_N);   // 是否闪烁
const starGlow  = new Uint8Array(STAR_N);   // 是否用柔光晕
const starOrder = new Uint16Array(STAR_N);

(function seedStars() {
  for (let i = 0; i < STAR_N; i++) {
    const u  = Math.random() * 2 - 1;                  // 球面均匀采样
    const th = Math.random() * Math.PI * 2;
    const s  = Math.sqrt(1 - u * u);
    const r  = STAR_R_MIN + Math.random() * (STAR_R_MAX - STAR_R_MIN);
    starPos[i * 3]     = r * s * Math.cos(th);
    starPos[i * 3 + 1] = r * s * Math.sin(th);
    starPos[i * 3 + 2] = r * u;

    // 三层亮度：绝大多数暗、少量中亮、极少数带光晕 —— 星空的“动态范围”
    const roll = Math.random();
    if (roll < 0.84) {            // 暗星主体，不抢知识节点
      starAlpha[i] = 0.16 + Math.random() * 0.18;
      starSize[i]  = 0.55 + Math.random() * 0.70;
    } else if (roll < 0.96) {     // 中亮星
      starAlpha[i] = 0.34 + Math.random() * 0.22;
      starSize[i]  = 1.15 + Math.random() * 0.85;
    } else {                      // 亮星：柔光晕
      starAlpha[i] = 0.55 + Math.random() * 0.28;
      starSize[i]  = 1.90 + Math.random() * 1.20;
      starGlow[i]  = 1;
    }
    starPhase[i] = Math.random() * Math.PI * 2;
    starTwk[i]   = starGlow[i];                        // 只让亮星轻微闪烁
  }
  // 按亮度排序：渲染时暗星可整桶设置 globalAlpha，把状态切换从 N 次压到几次
  const idx = new Array(STAR_N);
  for (let i = 0; i < STAR_N; i++) idx[i] = i;
  idx.sort((a, b) => starAlpha[a] - starAlpha[b]);
  for (let i = 0; i < STAR_N; i++) starOrder[i] = idx[i];
})();

// 亮星柔光精灵：一次性预渲染，之后 drawImage 复用
const starGlowSprite = (function () {
  const S = 64, c = document.createElement('canvas');
  c.width = c.height = S;
  const g = c.getContext('2d');
  const grd = g.createRadialGradient(S / 2, S / 2, 0, S / 2, S / 2, S / 2);
  grd.addColorStop(0.00, 'rgba(232,242,255,1)');
  grd.addColorStop(0.20, 'rgba(159,196,255,0.72)');
  grd.addColorStop(0.52, 'rgba(122,162,236,0.16)');
  grd.addColorStop(1.00, 'rgba(122,162,236,0)');
  g.fillStyle = grd;
  g.fillRect(0, 0, S, S);
  return c;
})();

const starCanvas = el('stars');
const starCtx = starCanvas.getContext('2d');
let starDpr = 1;
let starLastCam = null;   // 上一帧相机矩阵，用于判断是否静止
let starIdleTick = 0;
function resizeStars() {
  starDpr = Math.min(2, window.devicePixelRatio || 1);
  starCanvas.width  = Math.floor(innerWidth  * starDpr);
  starCanvas.height = Math.floor(innerHeight * starDpr);
  starCanvas.style.width  = innerWidth + 'px';
  starCanvas.style.height = innerHeight + 'px';
  starLastCam = null;     // 尺寸变了必须强制重绘一次
}
resizeStars();

// 相机没动就不必整幅重绘；静止时降到约 1/3 帧率只维持亮星闪烁，
// 把 CPU 让给 WebGL 主画面（读图时明显省电）。
function cameraMoved(cam) {
  const e = cam.matrixWorld.elements;
  if (!starLastCam) { starLastCam = Array.prototype.slice.call(e); return true; }
  for (let i = 0; i < 16; i++) {
    if (Math.abs(e[i] - starLastCam[i]) > 1e-6) {
      starLastCam = Array.prototype.slice.call(e);
      return true;
    }
  }
  return false;
}

window.__starStats = { drawn: 0, ms: 0, total: STAR_N };

function drawStars(now) {
  requestAnimationFrame(drawStars);
  const cam = Graph.camera();
  if (!cam || !cam.matrixWorldInverse) return;
  if (!cameraMoved(cam)) {
    starIdleTick++;
    if (starIdleTick % 3 !== 0) return;                // 静止：~20fps
  } else {
    starIdleTick = 0;                                  // 运动中：满帧
  }
  const w = starCanvas.width, h = starCanvas.height;
  const inv = cam.matrixWorldInverse.elements;
  const fovK = (h / 2) / Math.tan((cam.fov * Math.PI / 180) / 2);
  const tSec = (now || 0) * 0.001;
  const t0 = performance.now();

  starCtx.clearRect(0, 0, w, h);
  starCtx.fillStyle = '#9fc4ff';

  let curBucket = -1;                                  // 已设置的亮度桶
  let drawn = 0;
  for (let k = 0; k < STAR_N; k++) {
    const i = starOrder[k];
    const x = starPos[i * 3], y = starPos[i * 3 + 1], z = starPos[i * 3 + 2];
    const cx = inv[0] * x + inv[4] * y + inv[8]  * z + inv[12];
    const cy = inv[1] * x + inv[5] * y + inv[9]  * z + inv[13];
    const cz = inv[2] * x + inv[6] * y + inv[10] * z + inv[14];
    if (cz > -1) continue;                             // 相机背后
    const sx = w / 2 + (cx / -cz) * fovK;
    const sy = h / 2 - (cy / -cz) * fovK;
    if (sx < -8 || sy < -8 || sx > w + 8 || sy > h + 8) continue;
    drawn++;

    const depth = Math.min(1, 1700 / -cz);             // 近大远小
    const rr = Math.max(1, starSize[i] * (0.55 + depth * 0.95) * starDpr);

    if (starGlow[i]) {                                 // 亮星：柔光晕 + 轻微闪烁
      let a = starAlpha[i];
      if (starTwk[i]) a *= 0.76 + 0.24 * Math.sin(tSec * 1.6 + starPhase[i]);
      starCtx.globalAlpha = Math.min(0.9, a);
      const d = rr * 4.5;
      starCtx.drawImage(starGlowSprite, sx - d / 2, sy - d / 2, d, d);
      curBucket = -1;
    } else {                                           // 暗星：整桶设一次 alpha
      const b = Math.min(STAR_BUCKETS - 1, (starAlpha[i] * STAR_BUCKETS) | 0);
      if (b !== curBucket) {
        starCtx.globalAlpha = (b + 0.5) / STAR_BUCKETS;
        curBucket = b;
      }
      starCtx.fillRect(sx, sy, rr, rr);
    }
  }
  starCtx.globalAlpha = 1;
  window.__starStats = { drawn: drawn, ms: performance.now() - t0, total: STAR_N };
}
requestAnimationFrame(drawStars);

// ---------- init ----------
// 让 WebGL 画布真正透明，才能透出底下的 CSS 渐变与星场
try {
  const r = Graph.renderer();
  if (r && r.setClearAlpha) r.setClearAlpha(0);
} catch (e) { /* 渲染器尚未就绪时忽略 */ }

Graph.d3Force('charge').strength(-95);

// Community clustering force: pull same-community nodes toward their shared
// centroid so each knowledge domain becomes a readable spatial cluster.
const _centroids = {};
function computeCentroids() {
  const acc = {};
  for (const n of nodes) {
    if (!isFinite(n.x)) continue;
    const a = acc[n.comm] || (acc[n.comm] = { x: 0, y: 0, z: 0, c: 0 });
    a.x += n.x; a.y += n.y; a.z += n.z; a.c++;
  }
  for (const k in acc) {
    _centroids[k] = { x: acc[k].x / acc[k].c, y: acc[k].y / acc[k].c, z: acc[k].z / acc[k].c };
  }
}
Graph.d3Force('cluster', function (alpha) {
  computeCentroids();
  const s = 0.16 * alpha;
  for (const n of nodes) {
    if (!nodeVisible(n)) continue;
    const c = _centroids[n.comm];
    if (!c) continue;
    n.vx = (n.vx || 0) + (c.x - n.x) * s;
    n.vy = (n.vy || 0) + (c.y - n.y) * s;
    n.vz = (n.vz || 0) + (c.z - n.z) * s;
  }
});

Graph.onEngineStop(() => Graph.zoomToFit(700, 60));
setTimeout(() => Graph.zoomToFit(1100, 70), 1600);
setTimeout(() => {
  const l = el('loading');
  l.style.opacity = '0';
  setTimeout(() => l.remove(), 520);
}, 900);
addEventListener('resize', () => {
  Graph.width(innerWidth).height(innerHeight);
  resizeStars();
});
Graph.width(innerWidth).height(innerHeight);
</script>
</body>
</html>
"""

stats = f"{len(nodes)} 个知识点 · {len(links)} 条关联 · {len(comm_names)} 个知识域"

# pick a label threshold that surfaces roughly the top ~22 hubs
label_min_deg = 6
for t in range(12, 2, -1):
    if sum(1 for n in nodes if n["deg"] >= t) >= 18:
        label_min_deg = t
        break
print(f"label threshold deg>={label_min_deg} -> "
      f"{sum(1 for n in nodes if n['deg'] >= label_min_deg)} labels")

doc = (TEMPLATE
       .replace("__LIB__", lib_js)
       .replace("__DATA__", data_js)
       .replace("__COLORS__", color_js)
       .replace("__STATS__", stats)
       .replace("__LABELMINDEG__", str(label_min_deg)))

target = OUT / "graph-3d.html"
target.write_text(doc, encoding="utf-8")
print(f"wrote {target}  ({target.stat().st_size:,} bytes)")
print(f"nodes={len(nodes)} links={len(links)} communities={len(comm_names)}")
print("has external refs:", "unpkg.com" in doc or "cdn." in doc)
for c in payload["communities"][:5]:
    print(f"   {c['count']:4d}  {c['name']}  {c['color']}")
