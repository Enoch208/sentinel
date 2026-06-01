import { useEffect, useMemo, useState } from "react";

import { Controls } from "./components/Controls";
import { Dossier } from "./components/Dossier";
import { ExplorePanel } from "./components/ExplorePanel";
import { Viewport, type Coach } from "./components/Viewport";
import type { Mode } from "./lib/view";
import { TOUR, nextTourStep, stateOf } from "./lib/view";
import { useEngineSocket } from "./lib/useEngineSocket";
import "./App.css";

const ENGINE_URL = "ws://127.0.0.1:8765/ws";

export default function App() {
  const engine = useEngineSocket(ENGINE_URL);
  const { status, frame, verdict, metric, twins, facet, report, map, send } =
    engine;
  const [mode, setMode] = useState<Mode>("watch");
  const [sensitivity, setSensitivity] = useState(0.5);
  const [zone, setZone] = useState("default");
  const [tourStep, setTourStep] = useState<number | null>(null);
  const [sawWarming, setSawWarming] = useState(false);

  const state = useMemo(() => stateOf(verdict), [verdict]);

  useEffect(() => {
    if (tourStep !== null) setMode(TOUR[tourStep].mode);
  }, [tourStep]);

  useEffect(() => {
    if (tourStep === null) return;
    if (verdict?.warming && !sawWarming) setSawWarming(true);
    const next = nextTourStep(tourStep, verdict, sawWarming);
    if (next !== tourStep) setTourStep(next);
  }, [verdict, tourStep, sawWarming]);

  useEffect(() => {
    if (mode === "explore") send({ type: "facet" });
  }, [mode, send]);

  const onSensitivity = (value: number) => {
    setSensitivity(value);
    send({ type: "sensitivity", value });
  };

  const teach = (label: "expected" | "anomaly") => {
    if (verdict) send({ type: "teach", frame_id: verdict.frame_id, label });
  };

  const onZone = (next: string) => {
    setZone(next);
    send({ type: "zone", zone: next });
  };

  const coach: Coach | null =
    tourStep === null
      ? null
      : {
          index: tourStep,
          total: TOUR.length,
          text: TOUR[tourStep].text,
          manual: TOUR[tourStep].auto === null,
          last: tourStep >= TOUR.length - 1,
        };

  const advanceTour = () =>
    setTourStep((step) =>
      step === null || step >= TOUR.length - 1 ? null : step + 1,
    );

  return (
    <div className="app">
      <header className="bar">
        <div className="brand">
          <img className="logo" src="/logo.png" alt="Sentinel" />
          <span className="name">Sentinel</span>
        </div>
        <span className={`status status--${status}`}>{status}</span>
      </header>

      <main className="stage">
        <Viewport
          status={status}
          frame={frame}
          state={state}
          coach={coach}
          onSkip={() => setTourStep(null)}
          onAdvance={advanceTour}
          onReconnect={engine.reconnect}
        />

        <aside className="panel">
          <button
            className="ghost show-how"
            onClick={() => {
              send({ type: "reset" });
              setMode("watch");
              setSawWarming(false);
              setTourStep(0);
            }}
          >
            show me how
          </button>

          <Controls
            mode={mode}
            onMode={setMode}
            sensitivity={sensitivity}
            onSensitivity={onSensitivity}
            canTeach={verdict !== null}
            onTeach={teach}
          />

          {mode === "explore" && (
            <ExplorePanel
              canQuery={verdict !== null}
              twins={twins}
              facet={facet}
              report={report}
              map={map}
              zone={zone}
              onZone={onZone}
              onTwins={() =>
                verdict &&
                send({ type: "twins", frame_id: verdict.frame_id, k: 4 })
              }
              onReport={() => send({ type: "report" })}
              onMap={() => send({ type: "map" })}
            />
          )}

          <Dossier verdict={verdict} metric={metric} />

          <button className="ghost reset" onClick={() => send({ type: "reset" })}>
            reset memory
          </button>
        </aside>
      </main>
    </div>
  );
}
