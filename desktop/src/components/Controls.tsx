import type { Mode } from "../lib/view";
import { MODES } from "../lib/view";

export function Controls({
  mode,
  onMode,
  sensitivity,
  onSensitivity,
  canTeach,
  onTeach,
}: {
  mode: Mode;
  onMode: (mode: Mode) => void;
  sensitivity: number;
  onSensitivity: (value: number) => void;
  canTeach: boolean;
  onTeach: (label: "expected" | "anomaly") => void;
}) {
  return (
    <>
      <div className="modes">
        {MODES.map((option) => (
          <button
            key={option}
            className={`chip ${mode === option ? "chip--on" : ""}`}
            onClick={() => onMode(option)}
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
            disabled={!canTeach}
            onClick={() => onTeach("expected")}
          >
            👍 expected
          </button>
          <button
            className="teach-btn teach-btn--down"
            disabled={!canTeach}
            onClick={() => onTeach("anomaly")}
          >
            👎 anomaly
          </button>
        </div>
      )}
    </>
  );
}
