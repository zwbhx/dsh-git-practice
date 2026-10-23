# -*- coding: utf-8 -*-
"""Conventional Commits 提交信息校验器。

用法：
    python scripts/commit_lint.py "feat(cli): 新增周清单生成器"   # 校验一条，通过 exit 0
    echo "feat: foo" | python scripts/commit_lint.py              # 从 stdin 读
    python scripts/commit_lint.py --file .git/COMMIT_EDITMSG      # 校验 commit 模板文件
    python scripts/commit_lint.py --types feat,fix ""             # 自定义允许的 type

规则（来自 Conventional Commits 1.0.0 + 本地团队约定）：
    <type>(<scope>): <subject>
    - type 必须在白名单内
    - scope 可省略；若给出则必须是 kebab-case（小写字母/数字/连字符）
    - 冒号必须是英文冒号且冒号后恰好一个空格
    - subject 不能为空、不超过 50 个字符、不以句号结尾
    - 破坏性变更用 `!` 标记，或在正文写 `BREAKING CHANGE:`
"""
from __future__ import annotations

import argparse
import re
import sys

DEFAULT_TYPES = (
    "feat", "fix", "docs", "style", "refactor",
    "perf", "test", "build", "ci", "chore", "revert",
)

# <type>(<scope>)!?: <subject>
PATTERN = re.compile(
    r"^(?P<type>[a-z]+)(?:\((?P<scope>[^)]*)\))?(?P<bang>!)?: (?P<subject>.*)$"
)
SCOPE_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")
MAX_SUBJECT = 50


def parse(message: str) -> dict:
    """拆解提交信息首行，返回 {type, scope, breaking, subject, matched}。"""
    first = (message or "").strip().splitlines()[0] if (message or "").strip() else ""
    m = PATTERN.match(first)
    if not m:
        return {"matched": False, "raw": first, "type": None,
                "scope": None, "breaking": False, "subject": ""}
    return {
        "matched": True,
        "raw": first,
        "type": m.group("type"),
        "scope": m.group("scope"),
        "breaking": bool(m.group("bang")),
        "subject": m.group("subject"),
    }


def validate(message: str, types: tuple[str, ...] = DEFAULT_TYPES) -> list[str]:
    """返回错误列表；空列表表示通过。"""
    errors: list[str] = []
    if not (message or "").strip():
        return ["提交信息为空"]

    info = parse(message)
    if not info["matched"]:
        errors.append(
            "首行不符合 `<type>(<scope>): <subject>` 格式，"
            f"实际：{info['raw']!r}"
        )
        return errors

    if info["type"] not in types:
        errors.append(f"type `{info['type']}` 不在白名单 {list(types)} 内")

    scope = info["scope"]
    if scope is not None and scope != "" and not SCOPE_PATTERN.match(scope):
        errors.append(f"scope `{scope}` 必须是 kebab-case（小写字母/数字/连字符）")

    subject = info["subject"]
    if not subject.strip():
        errors.append("subject 不能为空")
    elif len(subject) > MAX_SUBJECT:
        errors.append(f"subject 长度 {len(subject)} 超过 {MAX_SUBJECT} 字，请精简")
    if subject.endswith("。"):
        errors.append("subject 不要以句号结尾")

    if info["breaking"] and "BREAKING CHANGE:" not in message:
        # 仅提示级别，不阻断（本地约定：用 ! 也可以）
        pass
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="校验 Conventional Commits 提交信息")
    parser.add_argument("message", nargs="?", default=None, help="提交信息；省略则读 stdin")
    parser.add_argument("--file", default=None, help="从文件读取提交信息")
    parser.add_argument("--types", default=",".join(DEFAULT_TYPES), help="逗号分隔的 type 白名单")
    args = parser.parse_args(argv)

    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            message = fh.read()
    elif args.message is not None:
        message = args.message
    else:
        message = sys.stdin.read()

    types = tuple(t.strip() for t in args.types.split(",") if t.strip())
    errors = validate(message, types=types)
    if errors:
        print("[commit_lint] 不通过：")
        for err in errors:
            print(f"  - {err}")
        return 1

    info = parse(message)
    flag = " (破坏性变更)" if info["breaking"] else ""
    print(f"[commit_lint] 通过：type={info['type']}, scope={info['scope']}, "
          f"subject={len(info['subject'])}字{flag}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
