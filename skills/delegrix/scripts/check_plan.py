#!/usr/bin/env python3
"""Offline, advisory preflight of a proposed Delegrix worker plan.

This script NEVER starts workers, authenticates user consent or calls ForgeGuard/ForgeScope.
A plan's `authorization.explicit` is an assertion to verify against the live chat.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

IDENTIFIER = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,63}$")


def _positive_int(value: Any) -> bool:
    return type(value) is int and value > 0


def _nonnegative_int(value: Any) -> bool:
    return type(value) is int and value >= 0


def _path(value: Any) -> str | None:
    """Only explicit repository-relative POSIX paths; no glob/escape/URL expansion."""
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        return None
    if value.startswith("/") or ":" in value or "*" in value or "?" in value:
        return None
    parts = value.strip("/").split("/")
    if not parts or any(part in ("", ".", "..") or part.endswith((" ", ".")) for part in parts):
        return None
    return "/".join(parts)


def _overlaps(left: str, right: str) -> bool:
    # Conservative portable comparison: case-only differences can alias on Windows.
    left, right = left.casefold(), right.casefold()
    return left == right or left.startswith(right + "/") or right.startswith(left + "/")


def _goal_mapping(plan: dict, workers: list) -> list[str]:
    """Validate v2 criterion coverage, not evidence, permissions or completion."""
    errors: list[str] = []

    def report(code: str) -> None:
        if code not in errors:
            errors.append(code)

    goal = plan.get("goal")
    if not isinstance(goal, dict):
        return ["INVALID_GOAL"]
    criteria = goal.get("criteria")
    if not isinstance(criteria, list) or not criteria or len(criteria) > 128:
        return ["INVALID_GOAL"]
    declared: set[str] = set()
    required: set[str] = set()
    for criterion in criteria:
        if not isinstance(criterion, dict):
            report("INVALID_CRITERION")
            continue
        identifier = criterion.get("id")
        if (not isinstance(identifier, str) or not IDENTIFIER.fullmatch(identifier)
                or type(criterion.get("required")) is not bool):
            report("INVALID_CRITERION")
            continue
        if identifier in declared:
            report("DUPLICATE_CRITERION")
        declared.add(identifier)
        if criterion["required"]:
            required.add(identifier)

    covered: set[str] = set()

    def mapping(values: Any, *, nonempty: bool) -> None:
        if (not isinstance(values, list) or len(values) > 128
                or (nonempty and not values)):
            report("INVALID_CRITERION_MAPPING")
            return
        seen: set[str] = set()
        for value in values:
            if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
                report("INVALID_CRITERION_MAPPING")
                continue
            if value in seen:
                report("DUPLICATE_CRITERION_MAPPING")
            seen.add(value)
            if value not in declared:
                report("UNKNOWN_CRITERION")
            else:
                covered.add(value)

    mapping(goal.get("coordinator_criteria"), nonempty=False)
    for worker in workers:
        if isinstance(worker, dict):
            mapping(worker.get("criterion_ids"), nonempty=True)
    if required - covered:
        report("UNCOVERED_REQUIRED_CRITERION")
    return errors


def evaluate(plan: Any) -> list[str]:
    """Return stable diagnostic codes for unaccepted planning conditions."""
    errors: list[str] = []

    def report(code: str) -> None:
        if code not in errors:
            errors.append(code)

    if not isinstance(plan, dict) or type(plan.get("schema_version")) is not int or plan["schema_version"] not in (1, 2):
        return ["INVALID_SCHEMA"]
    workers = plan.get("workers")
    if not isinstance(workers, list) or len(workers) > 128:
        return ["INVALID_WORKERS"]
    approval = plan.get("authorization", {})
    project = plan.get("project", {})
    runtime = plan.get("runtime", {})
    for item in (approval, project, runtime):
        if not isinstance(item, dict):
            return ["INVALID_SCHEMA"]
    if workers and approval.get("explicit") is not True:
        report("NO_DECLARED_APPROVAL")
    prior_launched = plan.get("launches_so_far", 0)
    if not _nonnegative_int(prior_launched):
        report("INVALID_SCHEMA")
        prior_launched = 0
    total_launches = prior_launched + len(workers)
    max_authorized = approval.get("max_workers")
    if max_authorized is not None:
        if not _nonnegative_int(max_authorized):
            report("INVALID_SCHEMA")
        elif total_launches > max_authorized:
            report("AUTHORIZATION_LIMIT")
    max_project = project.get("max_total_workers")
    if max_project is not None:
        if not _positive_int(max_project):
            report("INVALID_SCHEMA")
        elif total_launches > max_project:
            report("PROJECT_LIMIT")
    max_runtime = runtime.get("max_total_workers")
    if max_runtime is not None:
        if not _positive_int(max_runtime):
            report("INVALID_SCHEMA")
        elif total_launches > max_runtime:
            report("RUNTIME_LIMIT")
    min_project = project.get("min_meaningful_workers", 0)
    if not _nonnegative_int(min_project):
        report("INVALID_SCHEMA")
    elif len(workers) < min_project:
        report("MINIMUM_NOT_PLANNED")

    review = plan.get("forgescope", {})
    if not isinstance(review, dict):
        return ["INVALID_SCHEMA"]
    analysis_only = review.get("active") is True and review.get("mode") == "analysis-only"

    ids: set[str] = set()
    deps: dict[str, list[str]] = {}
    writes: list[tuple[str, str]] = []
    for worker in workers:
        if not isinstance(worker, dict):
            report("INVALID_WORKER")
            continue
        identifier = worker.get("id")
        if not isinstance(identifier, str) or not IDENTIFIER.fullmatch(identifier):
            report("INVALID_WORKER")
            continue
        if identifier in ids:
            report("DUPLICATE_WORKER")
        ids.add(identifier)
        depth = worker.get("depth", 1)
        may_delegate = worker.get("may_delegate", False)
        if type(depth) is not int or depth != 1 or type(may_delegate) is not bool or may_delegate:
            report("NESTED_DELEGATION")
        mode = worker.get("mode")
        if mode not in ("read", "write"):
            report("INVALID_WORKER")
        paths = worker.get("write_paths", [])
        if not isinstance(paths, list):
            report("INVALID_SCOPE")
            paths = []
        if mode == "read" and paths:
            report("READ_ONLY_VIOLATION")
        if mode == "write" and not paths:
            report("MISSING_WRITE_SCOPE")
        if analysis_only and mode == "write":
            report("READ_ONLY_VIOLATION")
        for raw in paths:
            path = _path(raw)
            if path is None:
                report("INVALID_SCOPE")
            elif mode == "write":
                writes.append((identifier, path))
        dependencies = worker.get("depends_on", [])
        if not isinstance(dependencies, list) or any(not isinstance(x, str) for x in dependencies):
            report("INVALID_DEPENDENCY")
            dependencies = []
        deps[identifier] = dependencies

    for source, dependencies in deps.items():
        for target in dependencies:
            if target not in ids:
                report("MISSING_DEPENDENCY")
            elif target == source:
                report("DEPENDENCY_CYCLE")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            report("DEPENDENCY_CYCLE")
            return
        if node in visited:
            return
        visiting.add(node)
        for dependency in deps.get(node, []):
            if dependency in ids:
                visit(dependency)
        visiting.remove(node)
        visited.add(node)

    for identifier in sorted(ids):
        visit(identifier)

    for i, (owner, path) in enumerate(writes):
        for other_owner, other_path in writes[i + 1 :]:
            if owner != other_owner and _overlaps(path, other_path):
                report("OVERLAPPING_WRITES")
    if plan["schema_version"] == 2:
        for code in _goal_mapping(plan, workers):
            report(code)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path, help="JSON plan to preflight (not an authorization grant)")
    args = parser.parse_args()
    try:
        plan = json.loads(args.plan.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        parser.error(f"could not read JSON plan: {exc}")
    codes = evaluate(plan)
    if codes:
        print("BLOCKED:", ", ".join(codes))
        return 1
    print("PREFLIGHT PASS (structural checks only; live authorization and runtime capability unverified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
