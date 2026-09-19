# Graph Report - zyy  (2026-09-19)

## Corpus Check
- Corpus is ~1,003 words - fits in a single context window. You may not need a graph.

## Summary
- 280 nodes · 310 edges · 15 communities
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 16 edges (avg confidence: 0.83)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- 监控与可观测性体系
- 云平台与云服务
- 网络协议与排障
- 脚本开发与运维平台化
- Linux 系统管理
- 自动化运维与 CI/CD
- 数据库运维
- K8s 进阶与学习路径
- Kubernetes 核心对象
- 工程能力与求职准备
- 安全合规与主机加固
- 网络安全与性能调优
- Docker 容器基础
- Ansible 自动化
- Terraform 与 IaC

## God Nodes (most connected - your core abstractions)
1. `Kubernetes 核心` - 18 edges
2. `华为云（主）` - 15 edges
3. `Prometheus 体系` - 12 edges
4. `云计算运维知识树（SRE 方向）` - 11 edges
5. `Ansible（核心）` - 11 edges
6. `配置管理与 IaC` - 11 edges
7. `Docker` - 11 edges
8. `Linux 系统基础` - 10 edges
9. `关系型数据库` - 9 edges
10. `网络协议与模型` - 8 edges

## Surprising Connections (you probably didn't know these)
- `云计算运维知识树（SRE 方向）` --references--> `Linux 系统`  [EXTRACTED]
  云计算运维知识树.md → 云计算运维知识树.md  _Bridges community 7 → community 4_
- `云计算运维知识树（SRE 方向）` --references--> `云平台`  [EXTRACTED]
  云计算运维知识树.md → 云计算运维知识树.md  _Bridges community 7 → community 1_
- `云计算运维知识树（SRE 方向）` --references--> `安全`  [EXTRACTED]
  云计算运维知识树.md → 云计算运维知识树.md  _Bridges community 7 → community 10_
- `云计算运维知识树（SRE 方向）` --references--> `数据库`  [EXTRACTED]
  云计算运维知识树.md → 云计算运维知识树.md  _Bridges community 7 → community 6_
- `云计算运维知识树（SRE 方向）` --references--> `监控与可观测性`  [EXTRACTED]
  云计算运维知识树.md → 云计算运维知识树.md  _Bridges community 7 → community 0_

## Hyperedges (group relationships)
- **Kubernetes 核心学习闭环（组件→部署→排障→工具）** — 云计算运维知识树_架构与组件_apiserver_etcd_scheduler_kubelet_kube_proxy, 云计算运维知识树_集群部署_kubeadm_与二进制, 云计算运维知识树_常见故障排查_crashloopbackoff_pending_imagepullbackoff, 云计算运维知识树_kubectl_高阶技巧与_jsonpath, 云计算运维知识树_cce_云上托管_k8s_实战 [EXTRACTED 0.75]
- **CI/CD 交付流水线（流水线→工具→制品→发布策略）** — 云计算运维知识树_流水线概念与阶段划分, 云计算运维知识树_jenkins_安装_job_与_pipeline_语法, 云计算运维知识树_gitlab_ci_github_actions, 云计算运维知识树_制品仓库_nexus_harbor, 云计算运维知识树_蓝绿发布_灰度发布_滚动发布, 云计算运维知识树_发布回滚与变更管理 [EXTRACTED 0.75]
- **可观测性三支柱（指标/日志/链路）** — 云计算运维知识树_监控与可观测性_prometheus_体系, 云计算运维知识树_grafana_面板与变量_模板化仪表盘, 云计算运维知识树_日志采集_elk_efk, 云计算运维知识树_链路追踪_jaeger_skywalking, 云计算运维知识树_opentelemetry_统一采集 [INFERRED 0.75]

## Communities (15 total, 0 thin omitted)

### Community 0 - "监控与可观测性体系"
Cohesion: 0.08
Nodes (31): AOM/CES 云监控与告警, Exporter 体系 node_exporter/blackbox/mysqld, Grafana 面板与变量、模板化仪表盘, Jenkins 安装、Job 与 Pipeline 语法, Loki + Promtail 轻量日志方案, OpenTelemetry 统一采集, PromQL 查询与聚合, Provider / Resource / State 管理 (+23 more)

### Community 1 - "云平台与云服务"
Cohesion: 0.09
Nodes (26): AWS 核心服务对照（EC2/S3/VPC/IAM）, ECS 弹性云服务器与镜像/规格, ELB 弹性负载均衡, EVS 云硬盘与快照/备份, IaaS / PaaS / SaaS 与责任共担模型, IAM 权限与委托, OBS 对象存储与生命周期规则, SFS 文件存储 / SFS Turbo (+18 more)

### Community 2 - "网络协议与排障"
Cohesion: 0.08
Nodes (25): CDN 原理与回源, curl / dig / nslookup / openssl s_client, DHCP、ARP、ICMP 协议, DNS 解析流程与常见记录类型, HTTP/2、HTTP/3 特性, HTTP/HTTPS 协议与报文结构, IP 地址规划与子网划分 CIDR, LVS / HAProxy 四层负载 (+17 more)

### Community 3 - "脚本开发与运维平台化"
Cohesion: 0.09
Nodes (23): CLI 工具 Click/argparse 开发, jq / yq 处理 JSON 与 YAML, REST API 设计与调用, Web 框架实现运维后台, 代码规范 flake8/black/类型注解, 任务调度 Airflow / Celery, 内部工具与自助化平台, 函数库与公共模块封装 (+15 more)

### Community 4 - "Linux 系统管理"
Cohesion: 0.09
Nodes (22): Linux 系统, Linux 内核与调优, Linux 存储与文件, Linux 系统基础, LVM 逻辑卷扩展与快照, NFS / Samba 共享, RAID 原理（0/1/5/10）, sudo 与最小权限委派 (+14 more)

### Community 5 - "自动化运维与 CI/CD"
Cohesion: 0.10
Nodes (21): boto3 / 华为云 SDK 调用, CI/CD, Flask/FastAPI 写运维小工具与 API, GitLab CI / GitHub Actions, requests / paramiko 自动化, 制品仓库 Nexus / Harbor, 发布回滚与变更管理, 变量、条件、循环、函数 (+13 more)

### Community 6 - "数据库运维"
Cohesion: 0.10
Nodes (21): MHA / MGR 高可用, MongoDB 基础与副本集, MySQL 安装与基础配置, RDS 云数据库 MySQL, Redis 主从、哨兵、Cluster, Redis 数据类型与持久化 RDB/AOF, Redis 缓存穿透/击穿/雪崩, SQL 基础与常用查询 (+13 more)

### Community 7 - "K8s 进阶与学习路径"
Cohesion: 0.13
Nodes (18): 云计算运维知识树（云计算运维工程师 / SRE）, CCE 云上托管 K8s 实战, CCE 云容器引擎（K8s）, Helm Chart 编写与发布, Helm 包管理, Operator 与 CRD 概念, Service Mesh Istio 流量治理, 云计算运维知识树（SRE 方向） (+10 more)

### Community 8 - "Kubernetes 核心对象"
Cohesion: 0.12
Nodes (18): ConfigMap / Secret, Deployment / ReplicaSet / DaemonSet / StatefulSet, HPA/VPA 弹性伸缩, Ingress 与 Ingress Controller, kubectl 高阶技巧与 JSONPath, Namespace 与资源配额, NetworkPolicy 网络策略, Pod 生命周期与多容器模式 (+10 more)

### Community 9 - "工程能力与求职准备"
Cohesion: 0.12
Nodes (16): Git 工作流与 Code Review, 变更管理与发布流程, 容量规划与性能压测, 故障应急与值班响应, 文档编写（架构图、SOP、Runbook）, 混沌工程 ChaosBlade, 现场排障演示与白板架构题, 稳定性治理与应急预案 (+8 more)

### Community 10 - "安全合规与主机加固"
Cohesion: 0.13
Nodes (15): 传输加密 TLS 证书签发与续期, 供应链安全与依赖漏洞, 入侵排查（后门、异常进程、计划任务）, 基线核查脚本与自动化巡检, 备份加密与恢复演练, 安全, 主机与系统安全, 合规与流程 (+7 more)

### Community 11 - "网络安全与性能调优"
Cohesion: 0.15
Nodes (14): DDoS 防护与流量清洗, DNS 云解析 / WAF / DDoS 高防, eBPF / perf 深度性能分析, firewalld / iptables 规则, Linux 网络与性能, SELinux 策略与排障, SSH 免密、密钥管理与加固, VPN / 堡垒机 JumpServer (+6 more)

### Community 12 - "Docker 容器基础"
Cohesion: 0.18
Nodes (11): Compose 多容器编排, Dockerfile 编写与多阶段构建, Docker, 容器与镜像安全扫描, 容器安全（非 root、镜像扫描）, 容器日志与排障, 数据卷与数据持久化, 自定义网络 bridge/host/overlay (+3 more)

### Community 13 - "Ansible 自动化"
Cohesion: 0.20
Nodes (10): Ad-Hoc 常用模块 command/copy/file/yum, Ansible Vault 敏感信息加密, Ansible 大规模性能调优（forks/serial/strategy）, AWX / Ansible Tower 平台化, handlers、tags、条件与循环, Inventory 与主机清单管理, Playbook 编写与 YAML 语法, Roles 角色化组织与 Galaxy (+2 more)

### Community 14 - "Terraform 与 IaC"
Cohesion: 0.22
Nodes (9): Git 版本控制与分支协作, Kustomize 环境差异化, Module 拆分与复用, Pulumi / CloudFormation 对比认知, Terraform Cloud / Atlantis 流水线集成, Terraform 基础语法 HCL, 多环境 workspace 与变量管理, 配置管理与 IaC (+1 more)

## Ambiguous Edges - Review These
- `IAM 权限与委托` → `多账号与多环境隔离`  [AMBIGUOUS]
  云计算运维知识树.md · relation: semantically_similar_to

## Knowledge Gaps
- **188 isolated node(s):** `文件系统与目录树 FHS`, `用户/组与权限 rwx、umask、ACL`, `特殊权限 SUID/SGID/Sticky`, `sudo 与最小权限委派`, `进程与作业管理 ps/top/kill/nohup/jobs` (+183 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 189 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What is the exact relationship between `IAM 权限与委托` and `多账号与多环境隔离`?**
  _Edge tagged AMBIGUOUS (relation: semantically_similar_to) - confidence is low._
- **Why does `云计算运维知识树（SRE 方向）` connect `K8s 进阶与学习路径` to `监控与可观测性体系`, `云平台与云服务`, `网络协议与排障`, `脚本开发与运维平台化`, `Linux 系统管理`, `自动化运维与 CI/CD`, `数据库运维`, `工程能力与求职准备`, `安全合规与主机加固`?**
  _High betweenness centrality (0.818) - this node is a cross-community bridge._
- **Why does `自动化运维` connect `自动化运维与 CI/CD` to `Ansible 自动化`, `Terraform 与 IaC`, `K8s 进阶与学习路径`?**
  _High betweenness centrality (0.247) - this node is a cross-community bridge._
- **Why does `容器与编排` connect `K8s 进阶与学习路径` to `Kubernetes 核心对象`, `Docker 容器基础`?**
  _High betweenness centrality (0.202) - this node is a cross-community bridge._
- **What connects `文件系统与目录树 FHS`, `用户/组与权限 rwx、umask、ACL`, `特殊权限 SUID/SGID/Sticky` to the rest of the system?**
  _188 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `监控与可观测性体系` be split into smaller, more focused modules?**
  _Cohesion score 0.07526881720430108 - nodes in this community are weakly interconnected._
- **Should `云平台与云服务` be split into smaller, more focused modules?**
  _Cohesion score 0.09230769230769231 - nodes in this community are weakly interconnected._