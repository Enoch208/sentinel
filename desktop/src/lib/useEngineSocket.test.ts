import { act, renderHook } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { useEngineSocket } from "./useEngineSocket";

class FakeWebSocket {
  static instances: FakeWebSocket[] = [];
  static OPEN = 1;

  url: string;
  readyState = 0;
  sent: string[] = [];
  onopen: (() => void) | null = null;
  onclose: (() => void) | null = null;
  onerror: (() => void) | null = null;
  onmessage: ((event: { data: string }) => void) | null = null;

  constructor(url: string) {
    this.url = url;
    FakeWebSocket.instances.push(this);
  }

  send(data: string): void {
    this.sent.push(data);
  }

  close(): void {
    this.readyState = 3;
    this.onclose?.();
  }

  open(): void {
    this.readyState = FakeWebSocket.OPEN;
    this.onopen?.();
  }

  emit(payload: unknown): void {
    this.onmessage?.({ data: JSON.stringify(payload) });
  }
}

beforeEach(() => {
  FakeWebSocket.instances = [];
  vi.stubGlobal("WebSocket", FakeWebSocket);
});

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("useEngineSocket", () => {
  it("opens and routes events by type", () => {
    const { result } = renderHook(() => useEngineSocket("ws://test/ws"));
    const socket = FakeWebSocket.instances[0];

    act(() => socket.open());
    expect(result.current.status).toBe("open");

    act(() =>
      socket.emit({
        type: "verdict",
        frame_id: 9,
        ts: 1,
        score: 0.4,
        threshold: 0.9,
        flagged: true,
        warming: false,
        neighbors: [],
      }),
    );
    expect(result.current.verdict?.flagged).toBe(true);

    act(() =>
      socket.emit({
        type: "metric",
        fps: 12,
        embed_ms: 30,
        query_ms: 1,
        anomaly_ms: 31,
        memory_mb: 200,
        point_count: 5,
        quantized: false,
      }),
    );
    expect(result.current.metric?.fps).toBe(12);

    act(() =>
      socket.emit({
        type: "facet",
        facets: [{ zone: "bench", memory: 4, flags: 2 }],
      }),
    );
    expect(result.current.facet?.facets[0].zone).toBe("bench");
  });

  it("sends commands only when open", () => {
    const { result } = renderHook(() => useEngineSocket("ws://test/ws"));
    const socket = FakeWebSocket.instances[0];

    act(() => result.current.send({ type: "reset" }));
    expect(socket.sent).toHaveLength(0);

    act(() => socket.open());
    act(() => result.current.send({ type: "reset" }));
    expect(socket.sent).toContain(JSON.stringify({ type: "reset" }));
  });

  it("reconnect opens a fresh socket", () => {
    const { result } = renderHook(() => useEngineSocket("ws://test/ws"));
    const before = FakeWebSocket.instances.length;

    act(() => result.current.reconnect());
    expect(FakeWebSocket.instances.length).toBe(before + 1);
  });

  it("marks the connection closed on close", () => {
    const { result } = renderHook(() => useEngineSocket("ws://test/ws"));
    const socket = FakeWebSocket.instances[0];

    act(() => socket.open());
    act(() => socket.close());
    expect(result.current.status).toBe("closed");
  });
});
