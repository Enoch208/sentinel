export type NeighborDTO = { id: number; score: number };

export type FrameEvent = {
  type: "frame";
  frame_id: number;
  ts: number;
  jpeg: string;
};

export type VerdictEvent = {
  type: "verdict";
  frame_id: number;
  ts: number;
  score: number | null;
  threshold: number;
  flagged: boolean;
  warming: boolean;
  neighbors: NeighborDTO[];
};

export type MetricEvent = {
  type: "metric";
  fps: number;
  embed_ms: number;
  query_ms: number;
  anomaly_ms: number;
  memory_mb: number;
  point_count: number;
  quantized: boolean;
};

export type TwinsEvent = {
  type: "twins";
  frame_id: number;
  results: NeighborDTO[];
};

export type ZoneFacet = { zone: string; memory: number; flags: number };

export type FacetEvent = {
  type: "facet";
  facets: ZoneFacet[];
};

export type AckEvent = {
  type: "ack";
  command: string;
  ok: boolean;
  detail: string;
};

export type EngineEvent =
  | FrameEvent
  | VerdictEvent
  | MetricEvent
  | TwinsEvent
  | FacetEvent
  | AckEvent;

export type Command =
  | { type: "sensitivity"; value: number }
  | { type: "teach"; frame_id: number; label: "expected" | "anomaly" }
  | { type: "twins"; frame_id: number; k: number }
  | { type: "reset" }
  | { type: "export"; path: string }
  | { type: "zone"; zone: string }
  | { type: "facet" };
