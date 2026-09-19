# 云计算运维知识图谱 · 3D

把云计算运维 / SRE 方向的知识树，转成一张**可交互的 3D 知识图谱**。

单文件、离线、双击即用。

---

## 快速开始

下载 [`graph-3d.html`](./graph-3d.html)，用浏览器打开即可。

**无需服务器、无需联网、无外部依赖** —— three.js 与图谱数据全部内嵌在这一个文件里（约 1.39 MB）。

> GitHub 不会在线渲染 HTML，点文件只会看到源码。想直接看效果，可以下载后本地打开，或开启 GitHub Pages。

---

## 内容

| 指标 | 数值 |
|---|---|
| 知识点（节点） | **280** |
| 关联（边） | **310** |
| 知识域（社区） | **15** |
| 文件大小 | 1.39 MB（含内嵌库） |

15 个知识域：Linux 系统管理、网络协议与排障、云平台与云服务、Kubernetes 核心对象、K8s 进阶与学习路径、Docker 容器基础、Ansible 自动化、Terraform 与 IaC、自动化运维与 CI/CD、监控与可观测性体系、数据库运维、安全合规与主机加固、网络安全与性能调优、脚本开发与运维平台化、工程能力与求职准备。

---

## 交互

| 操作 | 效果 |
|---|---|
| 拖拽 | 旋转视角 |
| 滚轮 | 缩放 |
| 右键拖拽 | 平移 |
| 悬停节点 | 显示知识点详情 |
| 单击节点 | 高亮该节点及其邻居，相机推近 |
| 点击空白 | 取消高亮 |
| 搜索框 | 实时高亮匹配项，回车定位 |
| 右侧图例 | 按知识域开关过滤 |
| 显示名称 | 显示 29 个枢纽节点的标签 |
| 自动旋转 | 开关自动环绕 |

---

## 实现要点

这个项目不只是"把数据塞进现成组件"，几个关键问题都是自己解的。

### 1. 社区聚类力 —— 让 3D 图谱可读

纯力导向布局会把 280 个节点摊成一团，颜色分得清但看不出结构。这里加入了一个自定义 d3 力，把同一知识域的节点往各自质心收拢，各领域在空间上形成独立团簇。

### 2. 深空背景 —— CSS 渐变 + 透明 WebGL 画布

背景用 CSS 径向渐变实现（中心 `#121a33` → 外围 `#0a0f1f` → 边缘 `#05070d`），WebGL 画布通过 `backgroundColor('rgba(0,0,0,0)')` 与 `setClearAlpha(0)` 设为透明，让渐变和星场透出来。

### 3. 星场 —— 为什么没用 `THREE.Points`

打包版内部是 `window.THREE ? window.THREE : {…内置实现…}`：**它只读 `window.THREE`、从不给它赋值**，运行时实测 `typeof window.THREE === "undefined"`；且 `Points` / `PointsMaterial` 无法从场景图反推（场景里只有 Mesh 系对象）。

因此星场改用独立 2D 画布 + 相机 `matrixWorldInverse` 做真实透视投影，转动/缩放时视差是真正的 3D。星点分三层亮度（暗星主体 / 中亮 / 带柔光晕的亮星），柔光精灵一次性预渲染后 `drawImage` 复用；按亮度分桶渲染，把 `globalAlpha` 状态切换从 6000 次压到 8 次；相机静止时自动降频重绘。

**密度需按视野反推**：相机 FOV 50°，星点撒在全球面时大部分落在视野外 —— 1500 颗在屏幕上只剩约 70 颗。实测后调到 6000 颗，屏幕可见约 1500 颗。

### 4. 标签层

同样因为拿不到 `THREE`，标签用 `graph2ScreenCoords` 投影 + HTML 覆盖层实现。相机朝向从 `matrixWorld.elements` 手算 —— three 的 `Camera.getWorldDirection()` 会对返回值链式调用 `.negate()`，传入轻量替身对象会每帧抛异常。

---

## 数据来源

知识树源文件由人工维护，图谱数据通过 [Graphify](https://github.com/Graphify-Labs/graphify) 自动抽取：

```bash
pip install "graphifyy[terraform]"
python -m graphify . --update
```

抽取结果：95% 的边为 EXTRACTED（明确来自原文），5% 为 INFERRED。

---

## 许可证

- 本项目代码：MIT，见 [`LICENSE`](./LICENSE)
- 内嵌的第三方库：three.js r183、3d-force-graph v1.80.0（均为 MIT），完整声明见 [`THIRD-PARTY-NOTICES.md`](./THIRD-PARTY-NOTICES.md)
