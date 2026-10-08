// Browser-only counterpart of the threshold rules in agents/workers.py.
// This is not a hardware benchmark, cryptographic validation, or signed audit.
const ID_PATTERN = /^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$/;
const FLAGS = ["DISCORDANT", "ANOMALY", "MUTANT", "VIOLATION", "FAIL", "REJECT"];

export function evaluateTelemetry(input) {
  const taskId = String(input.task_id ?? "").trim();
  const targetId = String(input.target_identifier ?? "").trim();
  if (!ID_PATTERN.test(taskId) || !ID_PATTERN.test(targetId)) {
    throw new Error("Task and target IDs must contain 1–64 letters, digits, underscores, or hyphens, beginning with a letter or digit.");
  }
  const primary = Number(input.primary_metric);
  const secondary = Number(input.secondary_metric);
  if (!Number.isFinite(primary) || !Number.isFinite(secondary)) {
    throw new Error("Both numeric metrics must be finite numbers.");
  }
  if (typeof input.is_critical_flag !== "boolean") {
    throw new Error("Critical flag must be a boolean.");
  }
  const descriptor = String(input.status_descriptor ?? "");
  if (descriptor.length > 256) {
    throw new Error("Status descriptor must not exceed 256 characters.");
  }
  const alerts = [];
  function add(worker, urgency, summary, details, remediation) {
    alerts.push({
      origin_worker: worker, urgency, summary,
      technical_details: details, actionable_remediation: remediation
    });
  }
  if (primary > 25) {
    add("InvariantQCWorker", "ELEVATED_RISK", "Primary Metric Threshold Exceeded",
      `Primary measurement (${primary.toFixed(2)}) exceeds the configured threshold (25.00).`,
      "Review the primary metric and configured threshold.");
  }
  if (input.is_critical_flag || secondary > 12) {
    add("SafetyEscalationWorker", input.is_critical_flag ? "CRITICAL_STAT_PANIC" : "ELEVATED_RISK",
      "Critical Flag or Secondary Threshold Triggered",
      `CriticalFlag=${input.is_critical_flag}; secondary metric=${secondary.toFixed(2)}; threshold=12.00.`,
      "Investigate the triggering condition.");
  }
  if (FLAGS.some(flag => descriptor.toUpperCase().includes(flag))) {
    add("ProtocolConformanceWorker", "ELEVATED_RISK", "Descriptor Flag Detected",
      `Status descriptor matched an anomaly keyword: ${descriptor}`,
      "Review the supplied descriptor.");
  }
  const critical = alerts.some(a => a.urgency === "CRITICAL_STAT_PANIC");
  const elevated = alerts.length > 0;
  return {
    evaluation_type: "Local heuristic threshold assessment (not a hardware or compliance audit)",
    task_id: taskId, target_identifier: targetId,
    primary_metric: primary, secondary_metric: secondary,
    status_descriptor: descriptor, is_critical_flag: input.is_critical_flag,
    overall_urgency: critical ? "CRITICAL_STAT_PANIC" : elevated ? "ELEVATED_RISK" : "ROUTINE",
    integrity_status: critical ? "RECALIBRATION_REQUIRED" : elevated ? "DISCORDANT_ANOMALY" : "VALIDATED_OPTIMAL",
    total_alerts: alerts.length, critical_alerts_count: alerts.filter(a => a.urgency === "CRITICAL_STAT_PANIC").length,
    alerts
  };
}
