# -*- coding: utf-8 -*-
"""周例行清单生成器。

用法：
    python scripts/weekly_checklist.py             # 周一/周三/周五三段
    python scripts/weekly_checklist.py --month     # 追加月末复盘段
    python scripts/weekly_checklist.py --day 周三  # 只要某一天

设计目标：把「每天 5 分钟 / 每周 30 分钟 / 每月 1 小时」三档例行固化成可打印清单。
"""
from __future__ import annotations

import argparse
import sys

# 三档例行的最小可执行项（与 02_方法笔记.md 一一对应）
DAILY = [
    "看 1 次通知（Issue / PR / @我），能回就回，不能回就标 todo",
    "git status 确认工作区干净；有改动就写一个 WIP commit 或 stash",
    "给 1 个好项目点 star，或给 1 个仓库提 1 条 issue（练手）",
]

WEEKLY = {
    "周一": [
        "建本周 Issue：1 个目标 + 3 个子任务（勾选式验收标准）",
        "把本周产出目录新建好，README 写一句本周目标",
    ],
    "周三": [
        "切 feat/* 分支提交 1 个 PR（自己给自己 review 也要走流程）",
        "读一遍全量 diff：重点查密钥、大文件、调试代码",
    ],
    "周五": [
        "合并 PR（squash）→ 删分支 → 打 tag → 写 release notes",
        "更新 CHANGELOG.md 与 README「本周进展」",
    ],
}

MONTHLY = [
    "清理 stale 分支与超过 30 天未动的 Issue",
    "更新依赖与 Actions 主版本号（checkout / setup-python 等）",
    "复盘：本月合并几个 PR、卡在哪、下月目标 1 条",
    "把重复了 3 次以上的操作抽成脚本或模板",
]


def render(month: bool = False, only_day: str | None = None) -> str:
    """渲染清单为 markdown 文本。"""
    lines: list[str] = ["# GitHub 周例行清单", ""]
    lines.append("## 每天 5 分钟（碎片时间）")
    lines += [f"- [ ] {item}" for item in DAILY]
    lines.append("")

    days = [only_day] if only_day else list(WEEKLY)
    for day in days:
        if day not in WEEKLY:
            raise ValueError(f"未知的日期：{day}，可选：{'/'.join(WEEKLY)}")
        lines.append(f"## {day}（本周 30 分钟里的一块）")
        lines += [f"- [ ] {item}" for item in WEEKLY[day]]
        lines.append("")

    if month:
        lines.append("## 每月 1 小时（复盘）")
        lines += [f"- [ ] {item}" for item in MONTHLY]
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="生成 GitHub 周例行清单（markdown）")
    parser.add_argument("--month", action="store_true", help="追加月末复盘段")
    parser.add_argument("--day", default=None, help="只输出某一天，如 周三")
    parser.add_argument("--out", default=None, help="写入文件，默认打印到 stdout")
    args = parser.parse_args(argv)

    try:
        text = render(month=args.month, only_day=args.day)
    except ValueError as exc:
        print(f"[weekly_checklist] {exc}", file=sys.stderr)
        return 2

    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"[weekly_checklist] 已写入 {args.out}")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
