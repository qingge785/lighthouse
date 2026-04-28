---
name: lhdao-viewer
description: 查看并实时监控 Lighthouse (LHDao) 所有 Engagement 任务的状态、进度、已完成数量、消耗预算和价格（totalBudget / consumedBudget / remainingPool）。
version: 1.1
author: your-github-username
tags: [lhdai, lhdao, twitter, campaign, monitor, budget, price]
---

# LHDao 任务查看 & 实时价格监控

**功能**（仅查看，不创建任务）：
- 列出当前所有任务（支持按状态筛选）
- 查看单个任务的完整详情（含价格、预算消耗、剩余池、进度）
- 实时轮询多个任务的状态、进度、已完成数、消耗预算
- 自动高亮每个任务的**价格信息**（总预算、已消耗、剩余、平台手续费）

**直接在 OpenClaw 聊天里说下面任意一句话**：
- “查看我的 LHDao 所有任务”
- “监控我所有的 LHDao 任务价格”
- “实时轮询任务 ID: abc123 的状态和预算消耗”
- “列出所有 ACTIVE 状态的任务并显示价格”

**仓库地址**：https://github.com/qingge785/lighthouse

**加载方式**（推荐）：
1. 把本仓库完整 URL 粘贴到 OpenClaw 聊天框
2. 说：“安装这个 GitHub skill” 或 “use this github skill”

技能会自动读取 `lhdao_monitor.py` 执行查看和监控。
