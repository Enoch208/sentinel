import { useMemo, useState } from "react";

import type { VerdictEvent } from "./lib/types";
import { useEngineSocket } from "./lib/useEngineSocket";
import "./App.css";

const ENGINE_URL = "ws://127.0.0.1:8765/ws";
const MODES = ["watch", "teach", "explore"] as const;
type Mode = (typeof MODES)[number];

type ViewState = {
  key: "idle" | "warming" | "normal" | "flagged";
  label: string;
};

function stateOf(verdict: VerdictEvent | null): ViewState {
  if (!verdict) return { key: "idle", label: "waiting for the engine" };
  if (verdict.warming) return { key: "warming", label: "learning normal…" };
  if (verdict.flagged) return { key: "flagged", label: "⚠ out of place" };
  return { key: "normal", label: "normal" };
}

export default function App() {
  const { status, frame, verdict, metric, twins, send } =
    useEngineSocket(ENGINE_URL);
  const [mode, setMode] = useState<Mode>("watch");
  const [sensitivity, setSensitivity] = useState(0.5);

  const state = useMemo(() => stateOf(verdict), [verdict]);
  const score = verdict?.score ?? null;

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
          {frame ? (
            <img
              className="feed"
              src={`data:image/jpeg;base64,${frame.jpeg}`}
              alt="live perception"
            />
          ) : (
            <div className="empty">
              Show me your space — I’ll learn what’s normal and flag what isn’t.
            </div>
          )}
          <div className="badge">{state.label}</div>
        </section>

        <aside className="panel">
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
              label="embed"
              value={metric ? `${metric.embed_ms.toFixed(0)} ms` : "—"}
            />
            <Metric
              label="query"
              value={metric ? `${metric.query_ms.toFixed(1)} ms` : "—"}
            />
            <Metric
              label="memory"
              value={metric ? `${metric.point_count} pts` : "—"}
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
