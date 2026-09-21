#!/usr/bin/env python3
"""Fixture tests for validate_eval_criteria.py."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = REPO_ROOT / "scripts" / "validate_eval_criteria.py"


def write_runtime_reference(root: Path) -> None:
    references = root / "skills" / "java-functional-style" / "references"
    references.mkdir(parents=True)
    (references / "functional-style-examples.md").write_text(
        """# Runtime examples

```java
Map<String, Card> cardsById = cards.stream()
        .collect(Collectors.toMap(
                Card::id,
                Function.identity(),
                CardIndex::preferActive,
                LinkedHashMap::new));
```

```java
Profile profile = cachedProfile.orElseGet(() -> loadProfileFromRemote(userId));
```
""",
        encoding="utf-8",
    )


def write_scenario(
    root: Path,
    suite: str,
    name: str,
    task: str,
    *,
    invocation: str = "natural",
    task_type: str = "implementation",
    evidence_type: str | None = "ordinary_lift",
    rationale: str | None = None,
    checklist: list[dict[str, object]] | None = None,
) -> Path:
    scenario = root / suite / name
    scenario.mkdir(parents=True)
    (scenario / "task.md").write_text(task, encoding="utf-8")
    (scenario / "capability.txt").write_text("java-functional-style\n", encoding="utf-8")
    metadata: dict[str, object] = {"invocation": invocation, "task_type": task_type}
    if evidence_type is not None:
        metadata["evidence_type"] = evidence_type
    if rationale is not None:
        metadata["runtime_reference_overlap_rationale"] = rationale
    criteria = {
        "context": "Fixture scenario.",
        "type": "weighted_checklist",
        "checklist": checklist
        or [
            {
                "name": "Creates artifact",
                "category": "safety",
                "max_score": 5,
                "description": "Creates Example.java.",
            },
            {
                "name": "Preserves behavior",
                "category": "safety",
                "max_score": 5,
                "description": "Returns the requested output.",
            },
            {
                "name": "Uses functional style",
                "category": "functional_style",
                "max_score": 90,
                "description": "Uses clear callback code.",
            },
        ],
    }
    categories = {item["name"]: item.pop("category") for item in criteria["checklist"] if "category" in item}
    (scenario / "criteria.json").write_text(json.dumps(criteria, indent=2) + "\n", encoding="utf-8")
    (scenario / "criteria-meta.json").write_text(
        json.dumps({"metadata": metadata, "categories": categories}, indent=2) + "\n", encoding="utf-8"
    )
    return scenario


def identity_mapper_task(prefix: str = "Create `IdentityMapperCleanup.java`.") -> str:
    return f"""# Refactor callback mappers

{prefix} Assume Java 17.

```java
Map<String, Card> cardsById(List<Card> cards) {{
    return cards.stream()
            .collect(Collectors.toMap(
                    Card::id,
                    card -> card,
                    CardIndex::preferActive,
                    LinkedHashMap::new));
}}

record Card(String id) {{}}
```
"""


def supplier_task(prefix: str = "Create `review.md`.") -> str:
    return f"""# Review fallback laziness

{prefix} Assume Java 17.

```java
Profile profile = cachedProfile.orElse(loadProfileFromRemote(userId));
```
"""


class ValidateEvalCriteriaTests(unittest.TestCase):
    def run_validator(self, root: Path, *paths: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(VALIDATOR), *(str(path.relative_to(root)) for path in paths)],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )

    def with_repo(self):
        temp = tempfile.TemporaryDirectory()
        root = Path(temp.name)
        write_runtime_reference(root)
        return temp, root

    def test_main_ordinary_lift_overlap_fails(self) -> None:
        temp, root = self.with_repo()
        with temp:
            scenario = write_scenario(root, "evals", "01-overlap", identity_mapper_task())
            result = self.run_validator(root, scenario)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ordinary_lift is incompatible", result.stderr)

    def test_main_ordinary_lift_overlap_rationale_does_not_bypass(self) -> None:
        temp, root = self.with_repo()
        with temp:
            scenario = write_scenario(
                root,
                "evals",
                "01-overlap",
                identity_mapper_task(),
                rationale="Focused coverage kept intentionally.",
            )
            result = self.run_validator(root, scenario)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ordinary_lift is incompatible", result.stderr)

    def test_reference_ordinary_lift_overlap_fails(self) -> None:
        temp, root = self.with_repo()
        with temp:
            scenario = write_scenario(root, "evals-reference", "01-identity", identity_mapper_task())
            result = self.run_validator(root, scenario)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ordinary_lift is incompatible", result.stderr)

    def test_reference_focused_overlap_passes_with_rationale(self) -> None:
        temp, root = self.with_repo()
        with temp:
            scenario = write_scenario(
                root,
                "evals-reference",
                "01-identity",
                identity_mapper_task(),
                evidence_type="focused_reference",
                rationale="Allowed only as focused reference coverage.",
            )
            result = self.run_validator(root, scenario)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_regression_overlap_passes_when_classified_as_regression(self) -> None:
        temp, root = self.with_repo()
        with temp:
            scenario = write_scenario(
                root,
                "evals-regression",
                "01-identity-regression",
                identity_mapper_task(),
                evidence_type="solved_regression",
            )
            result = self.run_validator(root, scenario)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_task_names_skill_but_metadata_says_natural_fails(self) -> None:
        temp, root = self.with_repo()
        with temp:
            scenario = write_scenario(
                root,
                "evals-reference",
                "04-explicit",
                supplier_task("Use `$java-functional-style` to create `review.md`."),
                invocation="natural",
                evidence_type="focused_reference",
                rationale="Allowed only as focused reference coverage.",
            )
            result = self.run_validator(root, scenario)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("natural scenario explicitly invokes the skill", result.stderr)

    def test_task_names_skill_and_metadata_says_explicit_passes(self) -> None:
        temp, root = self.with_repo()
        with temp:
            scenario = write_scenario(
                root,
                "evals-reference",
                "04-explicit",
                supplier_task("Use `$java-functional-style` to create `review.md`."),
                invocation="explicit",
                task_type="review",
                evidence_type="focused_reference",
                rationale="Allowed only as focused reference coverage.",
            )
            result = self.run_validator(root, scenario)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_focused_identity_mapper_can_heavily_weight_behavior(self) -> None:
        temp, root = self.with_repo()
        checklist = [
            {
                "name": "Creates artifact",
                "category": "safety",
                "max_score": 5,
                "description": "Creates IdentityMapperCleanup.java.",
            },
            {
                "name": "Uses JDK identity functions",
                "category": "functional_style",
                "max_score": 80,
                "description": "Uses Function.identity for true identity mapper callbacks.",
            },
        ]
        with temp:
            scenario = write_scenario(
                root,
                "evals-reference",
                "01-to-map-function-identity-mapper",
                identity_mapper_task(),
                evidence_type="focused_reference",
                rationale="Allowed only as focused reference coverage.",
                checklist=checklist,
            )
            result = self.run_validator(root, scenario)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_rationale_for_focused_overlap_fails(self) -> None:
        temp, root = self.with_repo()
        with temp:
            scenario = write_scenario(
                root,
                "evals-reference",
                "01-identity",
                identity_mapper_task(),
                evidence_type="focused_reference",
            )
            result = self.run_validator(root, scenario)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("runtime-reference overlap must set", result.stderr)


if __name__ == "__main__":
    raise SystemExit(unittest.main())
