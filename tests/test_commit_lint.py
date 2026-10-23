# -*- coding: utf-8 -*-
"""unittest：commit_lint 解析与校验。"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import commit_lint as cl  # noqa: E402


class TestParse(unittest.TestCase):
    def test_with_scope(self):
        info = cl.parse("feat(cli): 新增周清单生成器")
        self.assertTrue(info["matched"])
        self.assertEqual(info["type"], "feat")
        self.assertEqual(info["scope"], "cli")
        self.assertFalse(info["breaking"])
        self.assertEqual(info["subject"], "新增周清单生成器")

    def test_without_scope(self):
        info = cl.parse("docs: 补充分支约定")
        self.assertTrue(info["matched"])
        self.assertIsNone(info["scope"])

    def test_breaking_bang(self):
        info = cl.parse("feat(api)!: 移除 v1 接口")
        self.assertTrue(info["breaking"])

    def test_not_matched(self):
        self.assertFalse(cl.parse("更新了一些东西")["matched"])
        self.assertFalse(cl.parse("feat:缺少空格")["matched"])


class TestValidate(unittest.TestCase):
    def test_ok(self):
        self.assertEqual(cl.validate("fix(lint): 修复空 scope 误报"), [])

    def test_bad_type(self):
        errors = cl.validate("update: 随便改改")
        self.assertTrue(any("不在白名单" in e for e in errors))

    def test_subject_too_long(self):
        errors = cl.validate("feat: " + "很" * 60)
        self.assertTrue(any("超过 50" in e for e in errors))

    def test_subject_trailing_period(self):
        errors = cl.validate("feat: 新增功能。")
        self.assertTrue(any("句号" in e for e in errors))

    def test_bad_scope(self):
        errors = cl.validate("feat(Bad Scope): 新增")
        self.assertTrue(any("kebab-case" in e for e in errors))

    def test_empty(self):
        self.assertEqual(cl.validate("   "), ["提交信息为空"])

    def test_custom_types(self):
        self.assertEqual(cl.validate("wip: 临时存档", types=("wip",)), [])


class TestScopeAllowlist(unittest.TestCase):
    """review 意见 R1 的回归用例：scope 白名单不能误杀合法提交。"""

    def test_scope_in_allowlist(self):
        self.assertEqual(cl.validate("feat(cli): 新增参数", scopes=("cli", "lint")), [])

    def test_scope_not_in_allowlist(self):
        errors = cl.validate("feat(api): 新增接口", scopes=("cli", "lint"))
        self.assertTrue(any("不在允许列表" in e for e in errors))

    def test_scope_less_commit_still_passes(self):
        # 关键回归：无 scope 的提交不该被 scope 白名单拦截
        self.assertEqual(cl.validate("docs: 补充约定", scopes=("cli", "lint")), [])

    def test_empty_allowlist_means_disabled(self):
        # 关键回归：空元组视为不启用，而不是「全部拒绝」
        self.assertEqual(cl.validate("docs: 补充约定", scopes=()), [])
        self.assertEqual(cl.validate("feat(api): 新增接口", scopes=()), [])

    def test_none_means_disabled(self):
        self.assertEqual(cl.validate("chore(deps): 升级依赖", scopes=None), [])


if __name__ == "__main__":
    unittest.main()
