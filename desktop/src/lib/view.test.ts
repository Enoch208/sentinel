import { describe, expect, it } from "vitest";

import type { VerdictEvent } from "./types";
import { TOUR, nextTourStep, stateOf } from "./view";

function verdict(overrides: Partial<VerdictEvent> = {}): VerdictEvent {
  return {
    type: "verdict",
    frame_id: 1,
    ts: 0,
    score: 0.9,
    threshold: 0.8,
    flagged: false,
    warming: false,
    neighbors: [],
    ...overrides,
  };
}

describe("stateOf", () => {
  it("is idle without a verdict", () => {
    expect(stateOf(null).key).toBe("idle");
  });

  it("reflects warming, flagged, and normal", () => {
    expect(stateOf(verdict({ warming: true })).key).toBe("warming");
    expect(stateOf(verdict({ flagged: true })).key).toBe("flagged");
    expect(stateOf(verdict()).key).toBe("normal");
  });
});

describe("nextTourStep", () => {
  it("stays null when inactive", () => {
    expect(nextTourStep(null, verdict())).toBeNull();
  });

  it("advances the learn step once warming ends", () => {
    expect(nextTourStep(0, verdict({ warming: true }))).toBe(0);
    expect(nextTourStep(0, verdict({ warming: false }))).toBe(1);
  });

  it("advances the flag step only when flagged", () => {
    expect(nextTourStep(1, verdict({ flagged: false }))).toBe(1);
    expect(nextTourStep(1, verdict({ flagged: true }))).toBe(2);
  });

  it("never auto-advances the manual steps", () => {
    expect(nextTourStep(2, verdict({ flagged: true }))).toBe(2);
    expect(nextTourStep(TOUR.length - 1, verdict({ flagged: true }))).toBe(
      TOUR.length - 1,
    );
  });
});
