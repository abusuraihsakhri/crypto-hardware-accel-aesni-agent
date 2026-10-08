import { evaluateTelemetry } from "./evaluator.mjs";

const form = document.querySelector("#audit-form");
const output = document.querySelector("#output");
const message = document.querySelector("#message");
const status = document.querySelector("#status");
const tasks = document.querySelector("#tasks");
const download = document.querySelector("#download");
let lastResult = null;
let processed = 0;

form.addEventListener("submit", event => {
  event.preventDefault();
  try {
    const data = new FormData(form);
    lastResult = evaluateTelemetry({
      task_id: data.get("task_id"),
      target_identifier: data.get("target_identifier"),
      primary_metric: data.get("primary_metric"),
      secondary_metric: data.get("secondary_metric"),
      status_descriptor: data.get("status_descriptor"),
      is_critical_flag: data.has("is_critical_flag")
    });
    processed += 1;
    tasks.textContent = String(processed);
    status.textContent = lastResult.overall_urgency.replaceAll("_", " ");
    output.textContent = JSON.stringify(lastResult, null, 2);
    message.textContent = "Evaluated locally. No network request was made.";
    message.className = "message";
    download.disabled = false;
  } catch (error) {
    lastResult = null;
    status.textContent = "INPUT ERROR";
    output.textContent = "No assessment generated.";
    message.textContent = error.message;
    message.className = "message error";
    download.disabled = true;
  }
});

download.addEventListener("click", () => {
  if (!lastResult) return;
  const blob = new Blob([JSON.stringify(lastResult, null, 2) + "\n"], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = "telemetry-assessment.json";
  document.body.append(anchor);
  anchor.click();
  anchor.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
});
