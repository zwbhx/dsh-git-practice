# Changelog

本文件格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

（下个版本的计划写这里，发版时整体挪到新版本段）

## [0.1.0] - 2026-10-23

首个可用版本：把「GitHub 常态化」里能固化的两件事做成脚本。

### Features

- **cli**：`scripts/weekly_checklist.py` 生成周例行清单，覆盖每天 5 分钟 / 每周 30 分钟 / 每月 1 小时三档，支持 `--day`、`--month`、`--out`。
- **lint**：`scripts/commit_lint.py` 校验 Conventional Commits，支持 type 白名单、scope 白名单、subject 长度与句号检查、stdin / 参数 / `--file` 三种输入。

### Bug Fixes

- **lint**：`--scopes` 白名单不再误杀「无 scope」的合法提交（如 `docs: 补充约定`）；空白名单视为不启用。
  _该问题由 v0.1.0 的模拟 review（意见 R1）发现，回归用例见 `tests/test_commit_lint.py::TestScopeAllowlist`。_

### Documentation

- 新增 `docs/分支与提交约定.md`：type 白名单表、scope 规则、分支命名、语义化版本、推送前 30 秒自查。
- README 补充快速开始与目录说明。

### CI

- 新增 `.github/workflows/ci.yml`：语法编译 + unittest + 提交信息检查，`permissions: contents: read`，矩阵覆盖 Python 3.10 / 3.12，main 分支额外产出构建产物。

### 已知限制

- 无远端仓库，`push`/PR 流程为本地模拟，未在真实 GitHub 上验证 Actions 运行。
- `commit_lint.py` 只校验首行与 subject，不解析正文的 `BREAKING CHANGE:` 语义。

---

### 版本对照（发版时怎么写的）

```bash
git tag -a v0.1.0 -m "v0.1.0: 首个可用版本（周清单 + 提交规范校验 + CI）"
git tag -l -n1
```
