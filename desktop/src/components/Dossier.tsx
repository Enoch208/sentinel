import type { MetricEvent, VerdictEvent } from "../lib/types";

export function Dossier({
  verdict,
  metric,
}: {
  verdict: VerdictEvent | null;
  metric: MetricEvent | null;
}) {
  const score = verdict?.score ?? null;
  return (
    <div className="dossier">
      <span className="eyebrow">on-device dossier</span>
      <Metric label="score" value={score === null ? "—" : score.toFixed(3)} />
      <Metric
        label="threshold"
        value={verdict ? verdict.threshold.toFixed(3) : "—"}
      />
      <Metric label="fps" value={metric ? metric.fps.toFixed(1) : "—"} />
      <Metric
        label="anomaly"
        value={metric ? `${metric.anomaly_ms.toFixed(0)} ms` : "—"}
      />
      <Metric
        label="embed"
        value={metric ? `${metric.embed_ms.toFixed(0)} ms` : "—"}
      />
      <Metric
        label="query"
        value={metric ? `${metric.query_ms.toFixed(1)} ms` : "—"}
      />
      <Metric
        label="footprint"
        value={metric ? `${metric.memory_mb.toFixed(0)} MB` : "—"}
      />
      <Metric
        label="memory"
        value={metric ? `${metric.point_count} pts` : "—"}
      />
      <Metric
        label="quantization"
        value={metric ? (metric.quantized ? "on · int8" : "off (local)") : "—"}
      />
    </div>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="metric">
      <span className="metric-label">{label}</span>
      <span className="metric-value">{value}</span>
    </div>
  );
}
