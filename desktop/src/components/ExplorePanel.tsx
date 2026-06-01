import type { FacetEvent, MapEvent, ReportEvent, TwinsEvent } from "../lib/types";

const ZONES = ["default", "bench", "shelf", "panel"] as const;

export function ExplorePanel({
  canQuery,
  twins,
  facet,
  report,
  map,
  zone,
  onZone,
  onTwins,
  onReport,
  onMap,
}: {
  canQuery: boolean;
  twins: TwinsEvent | null;
  facet: FacetEvent | null;
  report: ReportEvent | null;
  map: MapEvent | null;
  zone: string;
  onZone: (zone: string) => void;
  onTwins: () => void;
  onReport: () => void;
  onMap: () => void;
}) {
  return (
    <div className="explore">
      <button className="ghost" disabled={!canQuery} onClick={onTwins}>
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

      <span className="eyebrow">zone</span>
      <div className="modes">
        {ZONES.map((option) => (
          <button
            key={option}
            className={`chip ${zone === option ? "chip--on" : ""}`}
            onClick={() => onZone(option)}
          >
            {option}
          </button>
        ))}
      </div>
      <ul className="twins">
        {facet?.facets.map((entry) => (
          <li key={entry.zone}>
            <span>{entry.zone}</span>
            <span className="mono">
              {entry.memory} pts · {entry.flags} ⚠
            </span>
          </li>
        ))}
      </ul>

      <span className="eyebrow">watcher</span>
      <button className="ghost" onClick={onReport}>
        end-of-walk report
      </button>
      <ul className="twins">
        {report?.clusters.map((cluster) => (
          <li key={cluster.exemplar_id}>
            <span>cluster · {cluster.zones.join(", ") || "default"}</span>
            <span className="mono">×{cluster.size}</span>
          </li>
        ))}
      </ul>

      <span className="eyebrow">memory map</span>
      <button className="ghost" onClick={onMap}>
        project memory
      </button>
      {map && map.points.length > 0 && (
        <svg className="map" viewBox="-1.1 -1.1 2.2 2.2">
          {map.points.map((point) => (
            <circle
              key={`${point.flagged ? "a" : "n"}-${point.id}`}
              cx={point.x}
              cy={-point.y}
              r={point.flagged ? 0.05 : 0.025}
              className={point.flagged ? "node node--flag" : "node"}
            />
          ))}
        </svg>
      )}
    </div>
  );
}
