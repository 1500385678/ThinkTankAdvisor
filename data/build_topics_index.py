"""
build_topics_index.py
从 _ThinkTankLib/01-10 10 大主题 md 抽取元信息,生成 topics_index.json。

字段:id / name / category / roles / skills / source / updated_at / path
"""
import json
import re
from pathlib import Path

LIB_ROOT = Path(__file__).resolve().parents[2]  # _ThinkTankLib/
WEB_ROOT = Path(__file__).resolve().parents[1]  # ThinkTankWeb/
OUT_FILE = WEB_ROOT / "data" / "topics_index.json"


def parse_md(md_path: Path) -> dict:
    """解析单个主题 md 的元信息头(前 10 行内的 - **key**: value 格式)。"""
    text = md_path.read_text(encoding="utf-8")
    head = text.split("---", 1)[0]  # 取元信息头
    meta = {"name": md_path.stem}

    for line in head.splitlines():
        m = re.match(r"^- \*\*([^*]+)\*\*[::]\s*(.+)$", line.strip()) or \
            re.match(r"^- \*\*([^*]+)\*\*[：:]\s*(.+)$", line.strip())
        if not m:
            continue
        key, val = m.group(1).strip(), m.group(2).strip()
        if key == "类型":
            meta["category"] = val
        elif key == "适用角色":
            meta["roles"] = [s.strip() for s in re.split(r"/|、", val) if s.strip()]
        elif key == "关联技能":
            meta["skills"] = [s.strip() for s in re.split(r"/|、", val) if s.strip()]
        elif key == "更新日期":
            meta["updated_at"] = val
        elif key == "来源":
            meta["source"] = val
    return meta


def build_index() -> list[dict]:
    topics = []
    for i in range(1, 11):
        num = f"{i:02d}"
        dirs = sorted(LIB_ROOT.glob(f"{num}_*"))
        if not dirs:
            print(f"[WARN] 找不到 {num}_* 目录,跳过")
            continue
        d = dirs[0]
        mds = list(d.glob("*.md"))
        if not mds:
            print(f"[WARN] {d} 下无 md,跳过")
            continue
        md = mds[0]
        meta = parse_md(md)
        rel_path = md.relative_to(LIB_ROOT.parent).as_posix()  # 相对 _ThinkTankLib/ 父级
        topics.append({
            "id": num,
            "name": meta.get("name", md.stem),
            "category": meta.get("category", ""),
            "roles": meta.get("roles", []),
            "skills": meta.get("skills", []),
            "source": meta.get("source", ""),
            "updated_at": meta.get("updated_at", ""),
            "path": f"_ThinkTankLib/{rel_path.split('_ThinkTankLib/',1)[-1]}"
                      if "_ThinkTankLib/" in rel_path else rel_path,
        })
    return topics


def main() -> None:
    topics = build_index()
    OUT_FILE.write_text(
        json.dumps(topics, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"[OK] 写入 {OUT_FILE.relative_to(LIB_ROOT.parent)} · {len(topics)} 条")


if __name__ == "__main__":
    main()
