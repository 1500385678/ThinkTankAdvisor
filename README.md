# ThinkTankAdvisor

> 05-智库-ThinkTank 行业 Web 项目 · 内部代号 ThinkTankAdvisor
> 立项:2026-08-23 · 当前:Phase 0 资产盘点中

## 项目说明
基于张勇的 36 行业架构,ThinkTankAdvisor 是 **智库-ThinkTank** 行业的 Web 端顾问产品。
定位"政策研究者/企业战略师/投资人"三件套:研究方法 + 分析框架 + 行业简报。

## 项目状态

### Phase 进度(2026-09-03 巡检)

| Phase | 任务 | 进度 | 状态 |
|-------|------|------|------|
| **Phase 0 · 资产盘点** | 10 主题索引 | 1/6 | ✅ |
| | 50+ 实体抽取 | 50/50(100%) | ✅ 0828 完成 |
| | 图谱 schema | 3/6 | ✅ v0.1 完成(0903 迁移闭环) |
| | 议题分析框架模板 | 0/6 | ⚪ 未启动 |
| | 报告模板库 | 0/6 | ⚪ 未启动 |
| | SQLite → PG/Neo4j 迁移 | 0/6 | ⚪ 未启动 |
| **Phase 1 · MVP** | FastAPI 骨架 | 0/7 | ⚪ 未启动 |
| | React 前端 | 0/7 | ⚪ 未启动 |
| | 图谱可视化 | 0/7 | ⚪ 未启动 |
| | 议题分析引擎 | 0/7 | ⚪ 未启动 |
| | 报告生成器 | 0/7 | ⚪ 未启动 |
| | 飞书 OAuth | 0/7 | ⚪ 未启动 |
| | Docker Compose | 0/7 | ⚪ 未启动 |

### 知识资产
- **10 大主题索引**:`data/topics_index.json` ✅
- **图谱实体集**:`data/entities.json` · 50 实体 / 4 类型(book 10 / person 10 / concept 17 / event 13) / 86 关系 / 8 关系类型
- **图谱 schema**:`data/schema.json` v0.1 ✅(0903 闭环) · 迁移脚本:`scripts/migrate_entities.py` · 迁移输出:`data/entities_migrated.json`
- **方法论文档**:`_ThinkTankLib/01-10` 10 大主题 md
- **总纲**:`项目开发计划.md`(8.2 KB,v1.0) · **细则**:`智库顾问开发架构与计划.md`(20.6 KB,v1.0)

## 巡检历史
- 2026-09-03 · 工作树 clean,0902 巡检待办 #1 闭环(5d4ea39 README 刷),Phase 0 #3 仍卡草稿,50 实体未迁移,双计划挂账 8 天 → [.Log/巡检-智库-20260903.md](.Log/巡检-智库-20260903.md)
- 2026-09-02 · 工作树 clean,0901 schema.json v0.1 草稿业务首现(32e2796),Phase 0 进度 2.5/6(42%),README 表未刷挂账 1 天,0830 漏巡检挂账 3 天 → [.Log/巡检-智库-20260902.md](.Log/巡检-智库-20260902.md)
- 2026-09-01 · 工作树 clean,无业务推进(0828 实体抽取后 4 天无新 commit),仅 inspect 巡检 → [.Log/巡检-智库-20260901.md](.Log/巡检-智库-20260901.md)
- 2026-08-31 · `.gitignore fix` 已闭环(0828 bug 修),0830 漏巡检挂账,Phase 0/1 进度持平 → [.Log/巡检-智库-20260831.md](.Log/巡检-智库-20260831.md)
- 2026-08-29 · 实体抽取 50/50 后无业务推进,`.gitignore` `*.log` 误匹配 `.Log/` 待修 → [.Log/巡检-智库-20260829.md](.Log/巡检-智库-20260829.md)
- 2026-08-28 · 实体抽取达 50/50(0828 完成),余 5 项 Phase 0 挂账 → [.Log/巡检-智库-20260828.md](.Log/巡检-智库-20260828.md)
- 2026-08-27 · 实体抽取 60%,待补 20 实体 + 整合双计划 → [.Log/巡检-智库-20260827.md](.Log/巡检-智库-20260827.md)
- 2026-08-26 · 新增详细版架构方案,双计划并存待整合 → [.Log/巡检-智库-20260826.md](.Log/巡检-智库-20260826.md)
- 2026-08-25 · 修复 README.md git 冲突 → [.Log/巡检-智库-20260825.md](.Log/巡检-智库-20260825.md)

## 同步
- GitHub: https://github.com/1500385678/ThinkTankAdvisor
- Gitee: https://gitee.com/architectzy/ThinkTankAdvisor

## 自动化
- T1 每日 00:00 大计划协调
- T4 每日 02:00 项目巡检 + 写次日 plan
- T5 每日 03:00 小步开发 + commit + push

## 变更记录
- 2026-09-03 · 写 `scripts/migrate_entities.py` 跑通 50 实体按 schema v0.1 迁移(0 错误 / 86 关系),输出 `data/entities_migrated.json`,schema.status 升 "complete",Phase 0 #3 闭环(3/6 50%,巡检待办 #2 闭环)
- 2026-09-02 · README Phase 进度表刷 schema v0.1 草稿状态(0.5/6 🟡)+ 巡检历史追加 0901/0902(巡检待办 #1 闭环)
- 2026-09-01 · 起草 `data/schema.json` 知识图谱 4 顶层 schema 草稿(entity / relation / event / source,v0.1,0827 起挂账 #3 起步;待迁移 50 实体)
- 2026-08-31 · README 巡检历史补 0829/0831 两条 + 变更记录补 0829 `.gitignore fix`(巡检待办 #2 闭环)
- 2026-08-29 · `.gitignore` 加 `!.Log/` 反向规则,显式豁免巡检目录(`*.log` 误匹配 bug 修复)
- 2026-08-28 · 实体抽取达成 50/50(补 e020 张勇 / e027-e030 创新&框架概念 / e036-e043 中美政策事件 / e044-e050 智库方法论),Phase 0 checkbox 2/6 完成
- 2026-08-27 · .gitignore 完善(屏蔽 .plan/ .env* .db 等) + README 加 Phase 进度条
- 2026-08-26 · 新增 `data/entities.json` 30 实体/4 类型/46 关系
- 2026-08-25 · 修复 README.md git 冲突标记(保留 HEAD 详细版)
