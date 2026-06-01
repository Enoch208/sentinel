import { SectionHeading } from "@/components/ui/primitives";
import { LOOP_CARDS, LOOP_INTRO, type LoopCard } from "@/lib/content";
import { ICON_BOX, layout, surface, type } from "@/lib/tokens";

export function Loop() {
  return (
    <section
      id="loop"
      className={`${layout.container} ${layout.sectionX} ${layout.sectionYTight}`}
    >
      <SectionHeading
        marker={LOOP_INTRO.marker}
        title={LOOP_INTRO.title}
        body={LOOP_INTRO.body}
      />

      <div className={`mt-14 grid md:grid-cols-3 ${layout.gridGap}`}>
        {LOOP_CARDS.map((card, i) => (
          <Card key={card.step} card={card} delay={i * 90} />
        ))}
      </div>
    </section>
  );
}

function Card({ card, delay }: { card: LoopCard; delay: number }) {
  const Icon = card.icon;
  return (
    <div
      data-scroll-reveal
      style={{ ["--scroll-delay" as string]: `${delay}ms` }}
      className={`group relative overflow-hidden rounded-[18px] ${surface.panel} ${surface.panelHover} ${layout.cardP}`}
    >
      <div className="flashlight-bg absolute inset-0 pointer-events-none" />
      <div className="relative">
        <div className="flex items-center justify-between">
          <div className={surface.iconBox}>
            <Icon size={ICON_BOX} className="text-white/80" />
          </div>
          <span className="font-mono text-[11px] uppercase tracking-[0.22em] text-amber-300/70">
            {card.step}
          </span>
        </div>
        <h3 className={`${type.h3} mt-6`}>{card.title}</h3>
        <p className={`${type.body} mt-3`}>{card.blurb}</p>
      </div>
    </div>
  );
}
