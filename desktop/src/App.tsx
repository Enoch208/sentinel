import { useEffect, useMemo, useState } from "react";

import type { Mode } from "./lib/view";
import { MODES, TOUR, nextTourStep, stateOf } from "./lib/view";
import { useEngineSocket } from "./lib/useEngineSocket";
import "./App.css";

const ENGINE_URL = "ws://127.0.0.1:8765/ws";
const ZONES = ["default", "bench", "shelf", "panel"] as const;

export default function App() {
  const { status, frame, verdict, metric, twins, facet, report, send, reconnect } =
    useEngineSocket(ENGINE_URL);
  const [mode, setMode] = useState<Mode>("watch");
  const [sensitivity, setSensitivity] = useState(0.5);
  const [zone, setZone] = useState<string>("default");
  const [tourStep, setTourStep] = useState<number | null>(null);

  const state = useMemo(() => stateOf(verdict), [verdict]);
  const score = verdict?.score ?? null;

  useEffect(() => {
    if (tourStep !== null) setMode(TOUR[tourStep].mode);
  }, [tourStep]);

  useEffect(() => {
    if (mode === "explore") send({ type: "facet" });
  }, [mode, send]);

  useEffect(() => {
    if (tourStep === null) return;
    const next = nextTourStep(tourStep, verdict);
    if (next !== tourStep) setTourStep(next);
  }, [verdict, tourStep]);

  const onSensitivity = (value: number) => {
    setSensitivity(value);
    send({ type: "sensitivity", value });
  };

  const teach = (label: "expected" | "anomaly") => {
    if (verdict) send({ type: "teach", frame_id: verdict.frame_id, label });
  };

  const showTwins = () => {
    if (verdict) send({ type: "twins", frame_id: verdict.frame_id, k: 4 });
  };

  const advanceTour = () => {
    if (tourStep === null) return;
    setTourStep(tourStep >= TOUR.length - 1 ? null : tourStep + 1);
  };

  return (
    <div className="app">
      <header className="bar">
        <div className="brand">
          <span className="dot" />
          <span className="name">Sentinel</span>
        </div>
        <span className={`status status--${status}`}>{status}</span>
      </header>

      <main className="stage">
        <section className={`viewport viewport--${state.key}`}>
          {tourStep !== null && (
            <div className="coach">
              <span className="coach-step">
                {tourStep + 1}/{TOUR.length}
              </span>
              <p className="coach-text">{TOUR[tourStep].text}</p>
              <div className="coach-actions">
                <button className="ghost" onClick={() => setTourStep(null)}>
                  skip
                </button>
                {TOUR[tourStep].auto === null && (
                  <button className="ghost" onClick={advanceTour}>
                    {tourStep >= TOUR.length - 1 ? "done" : "next"}
                  </button>
                )}
              </div>
            </div>
          )}

          {status === "closed" ? (
            <div className="empty">
              <p className="empty-title">Engine offline</p>
              <p className="mono">cd engine &amp;&amp; uv run sentinel-serve</p>
              <button className="ghost" onClick={reconnect}>
                reconnect
              </button>
            </div>
          ) : frame ? (
            <img
              className="feed"
              src={`data:image/jpeg;base64,${frame.jpeg}`}
              alt="live perception"
            />
          ) : status === "open" ? (
            <div className="empty">
              Camera starting… if this hangs, grant camera permission to your
              terminal.
            </div>
          ) : (
            <div className="empty">Connecting to the engine…</div>
          )}

          {frame && <div className="badge">{state.label}</div>}
        </section>

        <aside className="panel">
          <button className="ghost show-how" onClick={() => setTourStep(0)}>
            show me how
          </button>

          <div className="modes">
            {MODES.map((option) => (
              <button
                key={option}
                className={`chip ${mode === option ? "chip--on" : ""}`}
                onClick={() => setMode(option)}
              >
                {option}
              </button>
            ))}
          </div>

          <div className="control">
            <label className="eyebrow" htmlFor="sensitivity">
              sensitivity
            </label>
            <input
              id="sensitivity"
              type="range"
              min={0}
              max={1}
              step={0.05}
              value={sensitivity}
              onChange={(event) => onSensitivity(Number(event.target.value))}
            />
          </div>

          {mode === "teach" && (
            <div className="teach">
              <button
                className="teach-btn teach-btn--up"
                disabled={!verdict}
                onClick={() => teach("expected")}
              >
                👍 expected
              </button>
              <button
                className="teach-btn teach-btn--down"
                disabled={!verdict}
                onClick={() => teach("anomaly")}
              >
                👎 anomaly
              </button>
            </div>
          )}

          {mode === "explore" && (
            <div className="explore">
              <button className="ghost" disabled={!verdict} onClick={showTwins}>
                show visual twins
              </button>
              <ul className="twins">
                {twins?.results.map((twin) => (
                  <li key={twin.id}>
                    <span>frame {twin.id}</span>
                    <span className="mono">{twin.score.toFixed(3)}</span>
                  </li>
                ))}
              </ul>

              <span className="eyebrow">zone</span>
              <div className="modes">
                {ZONES.map((option) => (
                  <button
                    key={option}
                    className={`chip ${zone === option ? "chip--on" : ""}`}
                    onClick={() => {
                      setZone(option);
                      send({ type: "zone", zone: option });
                    }}
                  >
                    {option}
                  </button>
                ))}
              </div>

              <ul className="twins">
                {facet?.facets.map((entry) => (
                  <li key={entry.zone}>
                    <span>{entry.zone}</span>
                    <span className="mono">
                      {entry.memory} pts · {entry.flags} ⚠
                    </span>
                  </li>
                ))}
              </ul>

              <span className="eyebrow">watcher</span>
              <button className="ghost" onClick={() => send({ type: "report" })}>
                end-of-walk report
              </button>
              <ul className="twins">
                {report?.clusters.map((cluster) => (
                  <li key={cluster.exemplar_id}>
                    <span>cluster · {cluster.zones.join(", ") || "default"}</span>
                    <span className="mono">×{cluster.size}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          <div className="dossier">
            <span className="eyebrow">on-device dossier</span>
            <Metric
              label="score"
              value={score === null ? "—" : score.toFixed(3)}
            />
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
              value={metric ? (metric.quantized ? "on" : "off (local)") : "—"}
            />
          </div>

          <button
            className="ghost reset"
            onClick={() => send({ type: "reset" })}
          >
            reset memory
          </button>
        </aside>
      </main>
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
