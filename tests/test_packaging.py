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

    def test_default_auto_activation_and_task_goal_contract(self):
        skill = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        guide = (SKILL / 'references' / 'integration-workflows.md').read_text(encoding='utf-8')
        goal = (SKILL / 'assets' / 'task-goal.md').read_text(encoding='utf-8')
        for token in ('ForgeGuard first', 'ForgeScope', 'Goal', 'host-activated',
                      'instructions-loaded', 'unavailable'):
            self.assertIn(token, skill + guide)
        self.assertLess(skill.index('**ForgeGuard first**'), skill.index('**Create or reuse a Goal'))
        self.assertLess(skill.index('**Create or reuse a Goal'), skill.index('**ForgeScope next**'))
        for token in ('Outcome:', 'Target:', 'Success criteria:', 'Evidence:',
                      'In scope:', 'Out of scope:', 'Stop / escalate:'):
            self.assertIn(token, goal)
        self.assertIn('Never create a separate task', goal)
        self.assertIn('does not grant permission', goal)

    def test_goal_architecture_contract_ships(self):
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        contract = (SKILL / "references" / "goal-architecture.md").read_text(encoding="utf-8")
        goal = (SKILL / "assets" / "task-goal.md").read_text(encoding="utf-8")
        self.assertIn("references/goal-architecture.md", skill)
        self.assertIn("../references/goal-architecture.md", goal)
        for fragment in ("Compatible active native goal", "Conflicting active goal",
                         "no usable native goal API", "ForgeGuard unavailable",
                         "do not create native goal state", "one authoritative representation",
                         "Apache-2.0"):
            self.assertIn(fragment, contract)

    def test_goal_v2_guidance_ships_and_is_routed(self):
        skill = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        architecture = (SKILL / "references" / "goal-architecture.md").read_text(encoding="utf-8")
        definition = (SKILL / "references" / "goal-definition.md").read_text(encoding="utf-8")
        lifecycle = (SKILL / "references" / "goal-lifecycle.md").read_text(encoding="utf-8")
        evaluation = (SKILL / "references" / "goal-evaluation.md").read_text(encoding="utf-8")
        template = (SKILL / "assets" / "task-goal.md").read_text(encoding="utf-8")
        for name in ("goal-definition.md", "goal-lifecycle.md", "goal-evaluation.md"):
            self.assertIn("references/" + name, skill)
            self.assertIn(name, architecture)
            self.assertIn("../references/" + name, template)
        for fragment in ("explicit goal-backed intent", "inspection error", "never blindly repeat creation",
                         "materially conflicting", "not a second authority"):
            self.assertIn(fragment, definition)
        for fragment in ("pending:", "passed:", "failed:", "blocked:", "stale:",
                         "invalidate affected previous evidence", "dirty worktree"):
            self.assertIn(fragment, lifecycle)
        for fragment in ("every mandatory criterion", "do not report completed",
                         "native completion cannot be confirmed", "not a test result"):
            self.assertIn(fragment, evaluation)

    def test_bundled_preflight_example(self):
        import json
        spec = importlib.util.spec_from_file_location("delegrix_example_check", SKILL / "scripts" / "check_plan.py")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        plan = json.loads((SKILL / "assets" / "preflight-example.json").read_text(encoding="utf-8"))
        self.assertEqual(mod.evaluate(plan), [])


if __name__ == "__main__":
    unittest.main()
