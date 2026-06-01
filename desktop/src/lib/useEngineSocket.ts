import { useCallback, useEffect, useRef, useState } from "react";

import type {
  Command,
  EngineEvent,
  FacetEvent,
  FrameEvent,
  MapEvent,
  MetricEvent,
  ReportEvent,
  TwinsEvent,
  VerdictEvent,
} from "./types";

export type ConnectionStatus = "connecting" | "open" | "closed";

export type EngineState = {
  status: ConnectionStatus;
  frame: FrameEvent | null;
  verdict: VerdictEvent | null;
  metric: MetricEvent | null;
  twins: TwinsEvent | null;
  facet: FacetEvent | null;
  report: ReportEvent | null;
  map: MapEvent | null;
  send: (command: Command) => void;
  reconnect: () => void;
};

export function useEngineSocket(url: string): EngineState {
  const [status, setStatus] = useState<ConnectionStatus>("connecting");
  const [frame, setFrame] = useState<FrameEvent | null>(null);
  const [verdict, setVerdict] = useState<VerdictEvent | null>(null);
  const [metric, setMetric] = useState<MetricEvent | null>(null);
  const [twins, setTwins] = useState<TwinsEvent | null>(null);
  const [facet, setFacet] = useState<FacetEvent | null>(null);
  const [report, setReport] = useState<ReportEvent | null>(null);
  const [map, setMap] = useState<MapEvent | null>(null);
  const [nonce, setNonce] = useState(0);
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const socket = new WebSocket(url);
    socketRef.current = socket;
    setStatus("connecting");

    socket.onopen = () => setStatus("open");
    socket.onclose = () => setStatus("closed");
    socket.onerror = () => setStatus("closed");
    socket.onmessage = (message: MessageEvent<string>) => {
      const event = JSON.parse(message.data) as EngineEvent;
      switch (event.type) {
        case "frame":
          setFrame(event);
          break;
        case "verdict":
          setVerdict(event);
          break;
        case "metric":
          setMetric(event);
          break;
        case "twins":
          setTwins(event);
          break;
        case "facet":
          setFacet(event);
          break;
        case "report":
          setReport(event);
          break;
        case "map":
          setMap(event);
          break;
        case "ack":
          break;
      }
    };

    return () => socket.close();
  }, [url, nonce]);

  const send = useCallback((command: Command) => {
    const socket = socketRef.current;
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify(command));
    }
  }, []);

  const reconnect = useCallback(() => setNonce((value) => value + 1), []);

  return {
    status,
    frame,
    verdict,
    metric,
    twins,
    facet,
    report,
    map,
    send,
    reconnect,
  };
}
