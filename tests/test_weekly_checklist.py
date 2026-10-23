# -*- coding: utf-8 -*-
"""unittest：weekly_checklist 渲染逻辑。"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts"))
import weekly_checklist as wc  # noqa: E402


class TestRender(unittest.TestCase):
    def test_default_contains_three_days(self):
        text = wc.render()
        for day in ("周一", "周三", "周五"):
            self.assertIn(day, text)
        self.assertNotIn("每月", text)

    def test_month_flag_appends_monthly(self):
        text = wc.render(month=True)
        self.assertIn("每月 1 小时", text)
        self.assertIn("清理 stale 分支", text)

    def test_only_day(self):
        text = wc.render(only_day="周三")
        self.assertIn("周三", text)
        self.assertNotIn("周一", text)
        self.assertNotIn("周五", text)

    def test_checkbox_format(self):
        text = wc.render()
        self.assertTrue(all(line.startswith("- [ ] ") for line in text.splitlines() if line.startswith("- [") ))

    def test_unknown_day_raises(self):
        with self.assertRaises(ValueError):
            wc.render(only_day="周八")


if __name__ == "__main__":
    unittest.main()
