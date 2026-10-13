"""Keep repository fixtures consistent with the implemented Python evaluator."""
import json
from pathlib import Path

import pytest

from agents.base import PHIGuard, SecurityException
from agents.models import SystemTaskPayload
from agents.supervisor import SystemSupervisor

ROOT = Path(__file__).resolve().parents[1]
DATASET = json.loads((ROOT / "benchmark_dataset.json").read_text(encoding="utf-8"))


@pytest.mark.parametrize("case", [case for case in DATASET["test_cases"] if "payload" in case],
                         ids=lambda case: case["case_id"])
def test_heuristic_reference_cases(case):
    dossier = SystemSupervisor().process_task(SystemTaskPayload(**case["payload"]))
    assert dossier.overall_urgency.value == case["expected_urgency"]
    assert dossier.integrity_status.value == case["expected_integrity"]
    assert dossier.standard_reference.startswith("Not assessed")


def test_sensitive_identifier_fixture_is_rejected():
    case = next(case for case in DATASET["test_cases"] if "adversarial_prompt" in case)
    assert case["expected_security_exception"]
    with pytest.raises(SecurityException):
        PHIGuard.assert_no_phi(case["adversarial_prompt"])


def test_standalone_openapi_document_matches_exposed_paths():
    document = json.loads((ROOT / "openapi_spec.json").read_text(encoding="utf-8"))
    assert set(document["paths"]) == {
        "/health", "/metrics", "/api/audit", "/api/chat", "/api/audit/logs"
    }
    assert "does not benchmark" in document["info"]["description"]
