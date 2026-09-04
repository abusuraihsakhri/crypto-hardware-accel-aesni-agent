"""
Automated Pytest Test Suite for Crypto Hardware Accel Aesni Agent.
Domain: Post-Quantum Cryptography & Hardware Security
Standard: NIST FIPS 203/204/205 / ISO/IEC 17825 Standards
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from agents.base import PHIGuard, AuditLogger, SecurityException, ValidationException, validate_identifier
from agents.models import SystemTaskPayload, UrgencyLevel, SystemIntegrityStatus
from agents.workers import InvariantQCWorker, SafetyEscalationWorker, ProtocolConformanceWorker
from agents.supervisor import SystemSupervisor
from cli import main


def test_phi_guard_enforcement():
    with pytest.raises(SecurityException):
        PHIGuard.assert_no_phi("Patient MRN-994827 blood culture positive for Staphylococcus")

    # Clean text passes
    PHIGuard.assert_no_phi("Analytical assay specimen KEY-001 optimal")


def test_specialized_workers():
    # Worker 1: QC Invariant
    p1 = SystemTaskPayload(task_id="T1", target_identifier="KEY-01", primary_metric=35.0)
    alerts1 = InvariantQCWorker.evaluate(p1)
    assert len(alerts1) == 1
    assert alerts1[0].urgency == UrgencyLevel.ELEVATED

    # Worker 2: Safety
    p2 = SystemTaskPayload(task_id="T2", target_identifier="KEY-02", primary_metric=10.0, is_critical_flag=True)
    alerts2 = SafetyEscalationWorker.evaluate(p2)
    assert len(alerts2) == 1
    assert alerts2[0].urgency == UrgencyLevel.CRITICAL_STAT

    # Worker 3: Protocol Conformance
    p3 = SystemTaskPayload(task_id="T3", target_identifier="KEY-03", primary_metric=10.0, status_descriptor="DISCORDANT_ANOMALY")
    alerts3 = ProtocolConformanceWorker.evaluate(p3)
    assert len(alerts3) == 1


def test_supervisor_consensus_and_audit():
    supervisor = SystemSupervisor(model_provider="mock")
    payload = SystemTaskPayload(
        task_id="TASK-PROD-01",
        target_identifier="KEY-PROD-01",
        primary_metric=12.0,
        secondary_metric=4.0,
        status_descriptor="NOMINAL"
    )
    dossier = supervisor.process_task(payload)
    assert dossier.overall_urgency == UrgencyLevel.ROUTINE
    assert dossier.integrity_status == SystemIntegrityStatus.VALIDATED
    assert dossier.audit_hash != ""

    # Verify cryptographic audit trail
    assert AuditLogger.verify_integrity() is True

    # CLI tests
    assert main(["audit", "--task-id", "CLI-TEST-01"]) == 0
    assert main(["chat", "Explain", "specifications"]) == 0
    assert main(["verify-audit"]) == 0


def test_input_validation():
    """Test that identifier validation works correctly."""
    # Valid identifiers
    assert validate_identifier("TASK-001") == "TASK-001"
    assert validate_identifier("KEY_01") == "KEY_01"
    assert validate_identifier("target-123") == "target-123"
    assert validate_identifier("A") == "A"

    # Invalid identifiers
    with pytest.raises(ValidationException):
        validate_identifier("")  # Empty

    with pytest.raises(ValidationException):
        validate_identifier("   ")  # Blank

    with pytest.raises(ValidationException):
        validate_identifier("task with spaces")  # Contains spaces

    with pytest.raises(ValidationException):
        validate_identifier("task@id!")  # Special characters

    with pytest.raises(ValidationException):
        validate_identifier("a" * 65)  # Too long


def test_supervisor_rejects_invalid_identifiers():
    """Test that supervisor rejects invalid task_id and target_identifier."""
    supervisor = SystemSupervisor(model_provider="mock")

    # Invalid task_id with spaces
    with pytest.raises(ValidationException):
        payload = SystemTaskPayload(
            task_id="invalid task id",
            target_identifier="KEY-01",
            primary_metric=12.0,
        )
        supervisor.process_task(payload)

    # Invalid target_identifier with special chars
    with pytest.raises(ValidationException):
        payload = SystemTaskPayload(
            task_id="TASK-01",
            target_identifier="key@invalid!",
            primary_metric=12.0,
        )
        supervisor.process_task(payload)


def test_batch_file_not_found():
    """Test that batch command handles missing file gracefully."""
    assert main(["batch", "-i", "nonexistent_file.csv"]) == 1
