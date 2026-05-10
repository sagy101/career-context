#!/usr/bin/env python3
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import check_template_safety


class TemplateSafetyTests(unittest.TestCase):
    def test_flags_generic_local_paths_and_token_shapes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            sample = root / "README.md"
            home_path = "/" + "Users/example/private.txt"
            token = "ghp_" + "abcdefghijklmnopqrstuvwxyz123456"
            sample.write_text(
                f"Use {home_path} and token {token}.\n",
                encoding="utf-8",
            )

            errors = check_template_safety.scan_paths(root)

        self.assertEqual(2, len(errors))
        self.assertIn("local user path", errors[0])
        self.assertIn("GitHub token", errors[1])

    def test_skips_local_forbidden_pattern_configuration(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            config = root / "config"
            config.mkdir()
            local = config / "local-forbidden-patterns.yaml"
            local.write_text("patterns:\n  - " + "/" + "Users/example\n", encoding="utf-8")

            errors = check_template_safety.scan_paths(root)

        self.assertEqual([], errors)


if __name__ == "__main__":
    unittest.main()
