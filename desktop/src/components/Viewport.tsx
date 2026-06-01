import type { ConnectionStatus } from "../lib/useEngineSocket";
import type { FrameEvent } from "../lib/types";
import type { ViewState } from "../lib/view";

export type Coach = {
  index: number;
  total: number;
  text: string;
  manual: boolean;
  last: boolean;
};

export function Viewport({
  status,
  frame,
  state,
  coach,
  onSkip,
  onAdvance,
  onReconnect,
}: {
  status: ConnectionStatus;
  frame: FrameEvent | null;
  state: ViewState;
  coach: Coach | null;
  onSkip: () => void;
  onAdvance: () => void;
  onReconnect: () => void;
}) {
  return (
    <section className={`viewport viewport--${state.key}`}>
      {coach && (
        <div className="coach">
          <span className="coach-step">
            {coach.index + 1}/{coach.total}
          </span>
          <p className="coach-text">{coach.text}</p>
          <div className="coach-actions">
            <button className="ghost" onClick={onSkip}>
              skip
            </button>
            {coach.manual && (
              <button className="ghost" onClick={onAdvance}>
                {coach.last ? "done" : "next"}
              </button>
            )}
          </div>
        </div>
      )}

      {status === "closed" ? (
        <div className="empty">
          <p className="empty-title">Engine offline</p>
          <p className="mono">cd engine &amp;&amp; uv run sentinel-serve</p>
          <button className="ghost" onClick={onReconnect}>
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
  );
}
