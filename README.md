云计算运维知识图谱
把云计算运维 / SRE 方向的知识树，用 Graphify 转成可查询、可交互的知识图谱。

内容
文件	说明
云计算运维知识树.md	知识源文件（人工维护，含 P0/P1/P2 求职优先级）
graphify-out/graph.json	图谱数据
graphify-out/graph-3d.html	3D 交互视图（离线单文件，双击即开）
graphify-out/graph.html	Graphify 官方 2D 交互视图
graphify-out/GRAPH_REPORT.md	图谱审计报告
图谱概览
280 个节点 · 310 条边 · 15 个知识域
95% EXTRACTED（明确来自原文）· 5% INFERRED
枢纽节点：Kubernetes 核心、华为云、Prometheus 体系、Ansible、Terraform/IaC
3D 视图
graph-3d.html 是自研的单文件查看器，完全离线（无 CDN 依赖）：

社区聚类力 —— 把同一知识域在空间上收拢成团；否则纯力导向布局会把 280 个点糊成一团
悬停详情、单击高亮邻居并推近、搜索定位、图例按知识域过滤、标签开关
标签层用 graph2ScreenCoords + HTML 覆盖层实现（three 的 standalone 包不导出 window.THREE，无法直接用 Sprite）
相机朝向从 matrixWorld.elements 手算 —— three 的 Camera.getWorldDirection() 对返回值链式调用 .negate()，传轻量替身对象会每帧抛异常
技术栈
Markdown · Graphify (Apache-2.0) · three.js / 3d-force-graph (MIT)

重建图谱
bash
复制
pip install "graphifyy[terraform]"
python -m graphify . --update
说明
知识树为个人整理的云计算运维/SRE 技能地图，优先级（P0/P1/P2）标注意在区分求职必要程度；图谱数据由 Graphify 从知识树自动抽取。
