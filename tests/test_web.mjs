import test from "node:test";
import assert from "node:assert/strict";
import { evaluateTelemetry } from "../web/evaluator.mjs";

const base = {
  task_id: "TASK-01", target_identifier: "KEY-01", primary_metric: 10,
  secondary_metric: 4, status_descriptor: "NOMINAL", is_critical_flag: false
};
test("nominal assessment matches Python threshold rules", () => {
  const result = evaluateTelemetry(base);
  assert.equal(result.overall_urgency, "ROUTINE");
  assert.equal(result.total_alerts, 0);
});
test("threshold boundaries are strict", () => {
  assert.equal(evaluateTelemetry({...base, primary_metric: 25, secondary_metric: 12}).total_alerts, 0);
  assert.equal(evaluateTelemetry({...base, primary_metric: 25.1, secondary_metric: 12.1}).total_alerts, 2);
});
test("critical flag overrides other urgency tiers", () => {
  const result = evaluateTelemetry({...base, is_critical_flag: true});
  assert.equal(result.overall_urgency, "CRITICAL_STAT_PANIC");
  assert.equal(result.critical_alerts_count, 1);
});
test("case-insensitive keyword flags", () => {
  assert.equal(evaluateTelemetry({...base, status_descriptor: "anomaly noted"}).total_alerts, 1);
});
test("bad identifiers and nonfinite metrics are rejected", () => {
  assert.throws(() => evaluateTelemetry({...base, task_id: "A B"}));
  assert.throws(() => evaluateTelemetry({...base, primary_metric: Infinity}));
  assert.throws(() => evaluateTelemetry({...base, secondary_metric: NaN}));
  assert.throws(() => evaluateTelemetry({...base, is_critical_flag: "false"}));
});
