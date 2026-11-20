"""Deterministic scenarios for a *proposed* Delegrix plan, not a live LLM evaluation."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "skills" / "delegrix" / "scripts" / "check_plan.py"
spec = importlib.util.spec_from_file_location("delegrix_preflight", MODULE)
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)


class PlanScenarios(unittest.TestCase):
    def test_fixture_cases(self):
        cases = json.loads((ROOT / "tests" / "fixtures" / "preflight_cases.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(cases), 15)
        for case in cases:
            with self.subTest(case=case["name"]):
                self.assertCountEqual(preflight.evaluate(case["plan"]), case["expect"])

    def test_rejects_bad_schema(self):
        self.assertEqual(preflight.evaluate({"schema_version": 2, "workers": []}), ["INVALID_SCHEMA"])
        self.assertEqual(preflight.evaluate({"schema_version": True, "workers": []}), ["INVALID_SCHEMA"])

    def test_not_a_live_authorization_verifier(self):
        # A syntactically valid `explicit` flag does not prove the user granted consent.
        plan = {"schema_version": 1, "authorization": {"explicit": True}, "workers": [{"id": "worker", "mode": "read"}]}
        self.assertEqual(preflight.evaluate(plan), [])


if __name__ == "__main__":
    unittest.main()
