# git-practice-repo · GitHub 常态化本地演练仓

> 这是「GitHub 常态化线」的**真实本地 git 仓库**，用于在无远端凭据的前提下，把
> commit / branch / review / merge / tag / CHANGELOG 全流程走一遍。
> 仓库内两个脚本都是可运行的 Python（标准库，无第三方依赖），并有 unittest 测试，
> 可直接被 `.github/workflows/ci.yml` 的 lint + test 步骤使用。

## 一句话定位

把「每周 GitHub 例行」做成一个能跑的小工具：`weekly_checklist.py` 生成清单，
`commit_lint.py` 卡住不规范的提交信息。

## 快速开始

```bash
python scripts/weekly_checklist.py            # 打印本周清单
python scripts/weekly_checklist.py --month    # 追加月末复盘段
python scripts/commit_lint.py "feat(cli): 新增周清单生成器"
python -m unittest discover -s tests -v       # 跑测试
```

## 目录

```
git-practice-repo/
├── README.md
├── .gitignore
├── CHANGELOG.md
├── docs/
│   └── 分支与提交约定.md
├── scripts/
│   ├── weekly_checklist.py
│   └── commit_lint.py
└── tests/
    ├── test_weekly_checklist.py
    └── test_commit_lint.py
```

## 约定

- 提交信息遵循 Conventional Commits，见 `docs/分支与提交约定.md`。
- 分支：`feat/*`、`fix/*`、`docs/*`、`chore/*`；合并后删除。
- 版本：语义化 `vMAJOR.MINOR.PATCH`，每次发版更新 `CHANGELOG.md`。

## 说明

仓库用户信息只做了**仓库级**配置（`git config user.name/user.email`），未修改全局配置；
没有任何远端（`git remote -v` 为空），所有操作纯本地。
