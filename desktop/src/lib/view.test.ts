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
    expect(nextTourStep(null, verdict(), true)).toBeNull();
  });

  it("does not advance the learn step from a stale normal verdict", () => {
    expect(nextTourStep(0, verdict({ warming: false }), false)).toBe(0);
  });

  it("advances the learn step only after warming, then normal", () => {
    expect(nextTourStep(0, verdict({ warming: true }), true)).toBe(0);
    expect(nextTourStep(0, verdict({ warming: false }), true)).toBe(1);
  });

  it("advances the flag step only when flagged", () => {
    expect(nextTourStep(1, verdict({ flagged: false }), true)).toBe(1);
    expect(nextTourStep(1, verdict({ flagged: true }), true)).toBe(2);
  });

  it("never auto-advances the manual steps", () => {
    expect(nextTourStep(2, verdict({ flagged: true }), true)).toBe(2);
    expect(nextTourStep(TOUR.length - 1, verdict({ flagged: true }), true)).toBe(
      TOUR.length - 1,
    );
  });
});
