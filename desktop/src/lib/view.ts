import type { VerdictEvent } from "./types";

export type Mode = "watch" | "teach" | "explore";
export const MODES: readonly Mode[] = ["watch", "teach", "explore"];

export type Advance = "settled" | "flagged" | null;
export type TourStep = { mode: Mode; text: string; auto: Advance };

export const TOUR: readonly TourStep[] = [
  {
    mode: "watch",
    text: "Sentinel is learning what's normal. Hold the scene steady for a few seconds.",
    auto: "settled",
  },
  {
    mode: "watch",
    text: "Now introduce something out of place — a tool, a hand, an object.",
    auto: "flagged",
  },
  {
    mode: "teach",
    text: "Caught it. Mark it 👍 expected or 👎 anomaly to tune what counts as normal.",
    auto: null,
  },
  {
    mode: "explore",
    text: "Open Explore to see its visual twins — everything that looks like this.",
    auto: null,
  },
];

export type ViewState = {
  key: "idle" | "warming" | "normal" | "flagged";
  label: string;
};

export function stateOf(verdict: VerdictEvent | null): ViewState {
  if (!verdict) return { key: "idle", label: "waiting for the engine" };
  if (verdict.warming) return { key: "warming", label: "learning normal…" };
  if (verdict.flagged) return { key: "flagged", label: "⚠ out of place" };
  return { key: "normal", label: "normal" };
}

export function nextTourStep(
  step: number | null,
  verdict: VerdictEvent | null,
  sawWarming: boolean,
): number | null {
  if (step === null) return null;
  const current = TOUR[step];
  const settled =
    current.auto === "settled" &&
    sawWarming &&
    verdict !== null &&
    !verdict.warming;
  const flagged = current.auto === "flagged" && verdict?.flagged === true;
  if (!settled && !flagged) return step;
  return step + 1 < TOUR.length ? step + 1 : null;
}
