import { SectionHeading } from "@/components/ui/primitives";
import { ENGINE_INTRO, ENGINE_ROWS, type EngineRow } from "@/lib/content";
import { ICON_BOX, layout, surface, type } from "@/lib/tokens";

export function Engine() {
  return (
    <section
      id="engine"
      className={`${layout.container} ${layout.sectionX} ${layout.sectionY}`}
    >
      <SectionHeading
        marker={ENGINE_INTRO.marker}
        title={ENGINE_INTRO.title}
        body={ENGINE_INTRO.body}
      />

      <div className="mt-14 rounded-[20px] border border-white/[0.07] bg-[#0a0a0c] overflow-hidden divide-y divide-white/[0.06]">
        {ENGINE_ROWS.map((row, i) => (
          <Row key={row.capability} row={row} delay={i * 70} />
        ))}
      </div>
    </section>
  );
}

function Row({ row, delay }: { row: EngineRow; delay: number }) {
  const Icon = row.icon;
  return (
    <div
      data-scroll-reveal
      style={{ ["--scroll-delay" as string]: `${delay}ms` }}
      className={`group grid grid-cols-1 md:grid-cols-[auto_minmax(0,1fr)_auto] items-start gap-4 md:gap-6 ${layout.cardP} ${surface.panelHover}`}
    >
      <div className="flex items-center gap-4">
        <div className={surface.iconBox}>
          <Icon size={ICON_BOX} className="text-white/80" />
        </div>
        <span className="[font-family:var(--font-display)] text-base md:text-lg font-light text-white md:w-[200px]">
          {row.capability}
        </span>
      </div>
      <p className={type.body}>{row.use}</p>
      <span className="font-mono text-[11px] uppercase tracking-[0.18em] text-amber-300/60 md:text-right whitespace-nowrap self-center">
        {row.note}
      </span>
    </div>
  );
}
