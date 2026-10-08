"""Regression tests for audit integrity and numeric input validation."""
import math
import pytest
from pydantic import ValidationError

from agents.base import AuditTrail
from agents.models import SystemTaskPayload


def test_ledger_recomputes_hmac_after_field_tampering():
    trail = AuditTrail(secret_key="test-only-secret")
    trail.log("supervisor", "supervisor", "TEST", {"count": 1})
    trail.log("supervisor", "supervisor", "TEST", {"count": 2})
    assert trail.verify_integrity()
    trail.logs[0]["event_type"] = "TAMPERED"
    assert not trail.verify_integrity()


def test_ledger_rejects_last_block_signature_tampering():
    trail = AuditTrail(secret_key="test-only-secret")
    trail.log("supervisor", "supervisor", "TEST", {"count": 1})
    trail.logs[-1]["current_hash"] = "0" * 64
    assert not trail.verify_integrity()


def test_ledger_snapshot_is_detached():
    trail = AuditTrail(secret_key="test-only-secret")
    trail.log("supervisor", "supervisor", "TEST", {"count": 1})
    snapshot = trail.get_trail()
    snapshot[0]["actor"] = "modified"
    assert trail.verify_integrity()
    assert trail.get_trail()[0]["actor"] == "supervisor"


@pytest.mark.parametrize("bad", [float("nan"), float("inf"), -float("inf")])
def test_invalid_floating_point_input_rejected(bad):
    with pytest.raises(ValidationError):
        SystemTaskPayload(task_id="TASK-01", target_identifier="KEY-01", primary_metric=bad)
    with pytest.raises(ValidationError):
        SystemTaskPayload(task_id="TASK-01", target_identifier="KEY-01", primary_metric=10, secondary_metric=bad)
