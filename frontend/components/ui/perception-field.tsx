import { cn } from "@/lib/cn";

export function PerceptionField({
  cols = 9,
  rows = 6,
  anomaly = 23,
  className,
}: {
  cols?: number;
  rows?: number;
  anomaly?: number;
  className?: string;
}) {
  const total = cols * rows;
  return (
    <div
      className={cn("group relative", className)}
      aria-hidden
      data-scroll-reveal
    >
      <div className="pointer-events-none absolute inset-x-6 top-0 h-px scan-line" />

      <div
        className="grid w-full gap-[14px] md:gap-[18px]"
        style={{ gridTemplateColumns: `repeat(${cols}, minmax(0, 1fr))` }}
      >
        {Array.from({ length: total }).map((_, i) => {
          const isAnomaly = i === anomaly;
          const calm = 0.1 + ((i * 37) % 13) / 90;
          return (
            <div
              key={i}
              className="relative flex items-center justify-center"
            >
              {isAnomaly ? (
                <span className="relative flex h-2.5 w-2.5 items-center justify-center">
                  <span className="absolute h-7 w-7 rounded-full border border-amber-300/50 sonar" />
                  <span className="h-2.5 w-2.5 rounded-full bg-amber-300 anomaly-pulse" />
                </span>
              ) : (
                <span
                  className="h-1.5 w-1.5 rounded-full bg-white"
                  style={{ opacity: calm }}
                />
              )}
            </div>
          );
        })}
      </div>

      <div
        className="pointer-events-none absolute"
        style={{
          left: `${((anomaly % cols) / cols) * 100}%`,
          top: `${(Math.floor(anomaly / cols) / rows) * 100}%`,
        }}
      >
        <div className="-translate-y-9 translate-x-3 whitespace-nowrap rounded-md border border-amber-300/30 bg-amber-300/5 px-2 py-1 font-mono text-[10px] uppercase tracking-[0.18em] text-amber-300/90 backdrop-blur-sm">
          ⚠ out of place
        </div>
      </div>
    </div>
  );
}
