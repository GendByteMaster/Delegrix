"""Validate the shipped Skill and its optional integrations (static evidence only)."""
import importlib.util
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "delegrix"


class PackageContract(unittest.TestCase):
    def test_static_validator(self):
        result = subprocess.run([sys.executable, str(SKILL / "scripts" / "validate.py")],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_integration_docs_ship(self):
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        integration = (SKILL / "references" / "integration-workflows.md").read_text(encoding="utf-8")
        for fragment in ("ForgeGuard", "ForgeScope", "AGENTS.md", "authorization", "integration-workflows.md"):
            self.assertIn(fragment, skill + integration)
        self.assertIn("analysis-only", integration)
        self.assertIn("unverified declaration", integration)

    def test_bundled_preflight_example(self):
        import json
        spec = importlib.util.spec_from_file_location("delegrix_example_check", SKILL / "scripts" / "check_plan.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        plan = json.loads((SKILL / "assets" / "preflight-example.json").read_text(encoding="utf-8"))
        self.assertEqual(mod.evaluate(plan), [])


if __name__ == "__main__":
    unittest.main()
