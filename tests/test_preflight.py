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
        self.assertEqual(preflight.evaluate({"schema_version": 3, "workers": []}), ["INVALID_SCHEMA"])
        self.assertEqual(preflight.evaluate({"schema_version": True, "workers": []}), ["INVALID_SCHEMA"])

    def test_goal_plan_v2(self):
        from copy import deepcopy

        example = json.loads((ROOT / "skills" / "delegrix" / "assets" /
                              "goal-preflight-example.json").read_text(encoding="utf-8"))
        self.assertEqual(preflight.evaluate(example), [])
        cases = [
            ("missing_goal", lambda p: p.pop("goal"), "INVALID_GOAL"),
            ("invalid_required", lambda p: p["goal"]["criteria"][0].update(required=1), "INVALID_CRITERION"),
            ("duplicate_id", lambda p: p["goal"]["criteria"].append({"id": "C1", "required": True}), "DUPLICATE_CRITERION"),
            ("unknown_id", lambda p: p["workers"][0].update(criterion_ids=["C99"]), "UNKNOWN_CRITERION"),
            ("duplicate_mapping", lambda p: p["workers"][0].update(criterion_ids=["C1", "C1"]), "DUPLICATE_CRITERION_MAPPING"),
            ("empty_mapping", lambda p: p["workers"][0].update(criterion_ids=[]), "INVALID_CRITERION_MAPPING"),
            ("malformed_mapping", lambda p: p["workers"][0].update(criterion_ids=[{}]), "INVALID_CRITERION_MAPPING"),
            ("uncovered_required", lambda p: p["goal"].update(coordinator_criteria=[]), "UNCOVERED_REQUIRED_CRITERION"),
            ("no_approval", lambda p: p["authorization"].update(explicit=False), "NO_DECLARED_APPROVAL"),
            ("budget", lambda p: p["authorization"].update(max_workers=1), "AUTHORIZATION_LIMIT"),
            ("nested", lambda p: p["workers"][0].update(depth=2), "NESTED_DELEGATION"),
            ("overlapping", lambda p: p["workers"][1].update(mode="write", write_paths=["src"]), "OVERLAPPING_WRITES"),
            ("analysis_only", lambda p: p.update(forgescope={"active": True, "mode": "analysis-only"}), "READ_ONLY_VIOLATION"),
            ("dependency_cycle", lambda p: p["workers"][0].update(depends_on=["review"]), "DEPENDENCY_CYCLE"),
        ]
        for name, mutate, expected in cases:
            with self.subTest(case=name):
                plan = deepcopy(example)
                mutate(plan)
                self.assertIn(expected, preflight.evaluate(plan))
        solo = deepcopy(example)
        solo["workers"] = []
        solo["goal"]["coordinator_criteria"] = ["C1", "C2", "C3"]
        self.assertEqual(preflight.evaluate(solo), [])

    def test_not_a_live_authorization_verifier(self):
        # A syntactically valid `explicit` flag does not prove the user granted consent.
        plan = {"schema_version": 1, "authorization": {"explicit": True}, "workers": [{"id": "worker", "mode": "read"}]}
        self.assertEqual(preflight.evaluate(plan), [])


if __name__ == "__main__":
    unittest.main()
