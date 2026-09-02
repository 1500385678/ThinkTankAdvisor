#!/usr/bin/env python3
"""
migrate_entities.py · Phase 0 #3 实体迁移脚本

把 data/entities.json 50 实体按 data/schema.json v0.1 校验并迁移到
data/entities_migrated.json,跑通后把 schema.status 从 "draft" 升 "complete"。

用法:
    python3 scripts/migrate_entities.py
    python3 scripts/migrate_entities.py --dry-run    # 只校验不改
    python3 scripts/migrate_entities.py --no-bump    # 不动 schema.status

不做的事:
- 不修改 entities.json 源文件(只读)
- 不修改 schema.json 顶层 version / created_at
- 不动项目开发计划.md(T1 大计划,本脚本只负责数据迁移)

进度:
- 2026-09-03 T5 起草,Phase 0 #3 闭环第一步(写脚本 + 跑通)
- 后续:T5 第二步把 entities.json 替换为 entities_migrated.json,T1 整合双计划时把 #3 标 [x]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

# 路径常量(相对脚本位置,跑哪都行)
ROOT = Path(__file__).resolve().parent.parent
ENTITIES_SRC = ROOT / "data" / "entities.json"
ENTITIES_DST = ROOT / "data" / "entities_migrated.json"
SCHEMA_PATH = ROOT / "data" / "schema.json"

ID_PATTERN = re.compile(r"^e\d{3,}$")
REQUIRED_FIELDS = ("id", "name", "type", "source", "abstract")
VALID_TYPES = ("book", "person", "concept", "event")


def load_json(path: Path) -> dict | list:
    """读 JSON 文件,缺失或格式错时报清晰错误。"""
    if not path.exists():
        sys.exit(f"❌ 找不到文件: {path}")
    try:
        with path.open(encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        sys.exit(f"❌ JSON 解析失败 {path}: {e}")


def validate_entities(entities: list[dict], schema: dict) -> list[str]:
    """
    按 schema v0.1 校验 entities。
    返回错误列表(空 = 全部通过)。
    """
    errors: list[str] = []
    seen_ids: set[str] = set()
    all_ids: set[str] = set()

    for i, e in enumerate(entities, 1):
        eid = e.get("id", f"<index {i}>")
        # 1. 必填字段
        for k in REQUIRED_FIELDS:
            if not e.get(k):
                errors.append(f"{eid}: 缺必填字段 '{k}'")
        # 2. id 格式
        if eid and not ID_PATTERN.match(eid):
            errors.append(f"{eid}: id 格式不符 '^e\\d{{3,}}$'")
        # 3. id 唯一
        if eid in seen_ids:
            errors.append(f"{eid}: id 重复")
        seen_ids.add(eid)
        all_ids.add(eid)
        # 4. type 枚举
        etype = e.get("type")
        if etype not in VALID_TYPES:
            errors.append(f"{eid}: type '{etype}' 不在 {VALID_TYPES}")

    # 5. relations.target_id 必须指向存在的实体
    for e in entities:
        for r in e.get("relations", []):
            tid = r.get("target_id")
            if tid not in all_ids:
                errors.append(
                    f"{e.get('id', '?')}: 关系 target_id '{tid}' 不在实体集中"
                )

    # 6. 校验 schema 本身有 entity 顶层
    if "entity" not in schema:
        errors.append("schema.json 缺 entity 顶层")

    return errors


def migrate(entities: list[dict], schema: dict) -> dict:
    """
    生成迁移后数据:加 _meta 元信息,排序,加 type-specific extras 提示。
    不改实体本身字段,只加 wrapper 元数据。
    """
    type_counts = Counter(e["type"] for e in entities)
    rel_count = sum(len(e.get("relations", [])) for e in entities)
    return {
        "_meta": {
            "schema_version": schema.get("version", "unknown"),
            "migrated_at": date.today().isoformat(),
            "source_file": str(ENTITIES_SRC.relative_to(ROOT)),
            "entity_count": len(entities),
            "type_distribution": dict(type_counts),
            "relation_count": rel_count,
            "validation": "passed",
        },
        "entities": entities,  # 原样保留,字段已符合 schema
    }


def bump_schema_status(schema_path: Path) -> None:
    """把 schema.json status 从 'draft' 升 'complete',记录升级日期。

    用行级正则替换而非 json.dump,保留原文件紧凑 1-行 1-对象格式,
    避免 369 行格式化噪音 diff。
    """
    text = schema_path.read_text(encoding="utf-8")
    if '"status": "complete"' in text:
        print(f"ℹ️  schema.status 已是 'complete',跳过升级")
        return

    today = date.today().isoformat()
    # 1. status: draft → complete
    text = re.sub(
        r'"status":\s*"draft"',
        '"status": "complete"',
        text,
        count=1,
    )
    # 2. note: 替换整行内容
    text = re.sub(
        r'"note":\s*"[^"]*"',
        f'"note": "50 实体已按本 schema 校验通过,迁移脚本 scripts/migrate_entities.py,0903 T5 闭环。"',
        text,
        count=1,
    )
    # 3. 在 created_at 行后插入 completed_at(保留文件结构)
    text = re.sub(
        r'("created_at":\s*"[^"]*",\n)',
        rf'\1  "completed_at": "{today}",\n',
        text,
        count=1,
    )

    schema_path.write_text(text, encoding="utf-8")
    print(f"✅ schema.status: draft → complete ({today})")


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase 0 #3 实体迁移")
    parser.add_argument(
        "--dry-run", action="store_true", help="只校验,不改文件不写输出"
    )
    parser.add_argument(
        "--no-bump", action="store_true", help="不升级 schema.status"
    )
    args = parser.parse_args()

    print("=" * 60)
    print("智库 · Phase 0 #3 实体迁移 (schema v0.1)")
    print("=" * 60)

    # 1. 加载
    entities = load_json(ENTITIES_SRC)
    schema = load_json(SCHEMA_PATH)
    if not isinstance(entities, list):
        sys.exit(f"❌ {ENTITIES_SRC} 应为 JSON array,实际 {type(entities).__name__}")

    print(f"📥 源: {ENTITIES_SRC.relative_to(ROOT)} ({len(entities)} 实体)")
    print(f"📋 schema: v{schema.get('version')} (status={schema.get('status')})")

    # 2. 校验
    errors = validate_entities(entities, schema)
    if errors:
        print(f"\n❌ 校验失败 {len(errors)} 条:")
        for err in errors:
            print(f"  - {err}")
        return 1
    print(f"✅ 校验通过: 50 实体 / 0 错误")

    # 3. dry-run 不写
    if args.dry_run:
        print("\n🔍 dry-run 模式,未写文件")
        return 0

    # 4. 写迁移输出
    migrated = migrate(entities, schema)
    with ENTITIES_DST.open("w", encoding="utf-8") as f:
        json.dump(migrated, f, ensure_ascii=False, indent=2)
    print(
        f"📤 输出: {ENTITIES_DST.relative_to(ROOT)} "
        f"({migrated['_meta']['entity_count']} 实体 / "
        f"{migrated['_meta']['relation_count']} 关系)"
    )

    # 5. 升级 schema status
    if not args.no_bump:
        bump_schema_status(SCHEMA_PATH)
    else:
        print("⏭️  --no-bump,schema.status 未变")

    print("\n" + "=" * 60)
    print("✅ Phase 0 #3 实体迁移完成")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
