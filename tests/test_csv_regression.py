"""Regression coverage for malformed CSVs, finite telemetry and API validation."""
import csv

import pytest
from fastapi import HTTPException

from cli import main as primary_main
from crypto_accel_aesni.cli import main as compatibility_main
from crypto_accel_aesni.agents import HardwareCryptoCoordinator
from crypto_accel_aesni.models import FrontierPayload
from agents.api import api_audit
from agents.models import SystemTaskPayload


@pytest.mark.parametrize("command", [primary_main, compatibility_main])
def test_batch_skips_invalid_records_and_keeps_good_rows(command, tmp_path):
    source = tmp_path / "records.csv"
    target = tmp_path / "result.csv"
    source.write_text(
        "task_id,target_identifier,primary_metric,secondary_metric,is_critical_flag,status_descriptor\n"
        "BAD ID,KEY-01,28,14,false,NOMINAL\n"
        "TASK-2,KEY-02,12,4,not-a-bool,NOMINAL\n"
        "TASK-3,KEY-03,12,4,false,NOMINAL,unexpected-cell\n"
        "TASK-4,KEY-04,12,4,false,NOMINAL\n",
        encoding="utf-8",
    )
    # The primary coordinator validates identifiers; both implementations validate
    # boolean flags and CSV column width.
    assert command(["batch", "-i", str(source), "-o", str(target)]) == 0
    with target.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if command is primary_main:
        assert [r["task_id"] for r in rows] == ["TASK-4"]
    else:
        assert [r["task_id"] for r in rows] == ["BAD ID", "TASK-4"]


@pytest.mark.parametrize("command", [primary_main, compatibility_main])
def test_batch_requires_expected_header(command, tmp_path):
    source = tmp_path / "invalid.csv"
    source.write_text("identifier,primary_metric\nTASK-1,25\n", encoding="utf-8")
    assert command(["batch", "-i", str(source), "-o", str(tmp_path / "out.csv")]) == 1


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf")])
def test_compatibility_coordinator_rejects_nonfinite_metrics(value):
    payload = FrontierPayload("TASK-1", "KEY-1", value, 1.0, "NOMINAL")
    with pytest.raises(ValueError, match="finite"):
        HardwareCryptoCoordinator().process(payload)


def test_primary_api_returns_validation_response_not_server_error():
    payload = SystemTaskPayload(task_id="TASK-1", target_identifier="KEY-1", primary_metric=1.0,
                                status_descriptor="MRN-994827")
    with pytest.raises(HTTPException) as error:
        api_audit(payload)
    assert error.value.status_code == 422
