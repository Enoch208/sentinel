import { SectionHeading } from "@/components/ui/primitives";
import { PERSONAS, PILLARS, WHO_MARKER, type Persona } from "@/lib/content";
import { ICON_BOX, layout, surface, type } from "@/lib/tokens";

export function Who() {
  return (
    <section
      id="who"
      className={`${layout.container} ${layout.sectionX} ${layout.sectionY}`}
    >
      <SectionHeading
        marker={WHO_MARKER}
        title={["The people who ask", "“what's out of place?”"]}
        body="Sentinel is built for jobs where the valuable signal is the unexpected — and where the network is slow, absent, or simply not trusted with what the camera sees."
      />

      <div className={`mt-14 grid sm:grid-cols-2 ${layout.gridGap}`}>
        {PERSONAS.map((p, i) => (
          <PersonaCard key={p.title} persona={p} delay={i * 70} />
        ))}
      </div>

      <div className={`mt-6 grid sm:grid-cols-2 lg:grid-cols-3 ${layout.gridGap}`}>
        {PILLARS.map((pillar, i) => {
          const Icon = pillar.icon;
          return (
            <div
              key={pillar.title}
              data-scroll-reveal
              style={{ ["--scroll-delay" as string]: `${i * 60}ms` }}
              className={`rounded-[18px] ${surface.panel} ${surface.panelHover} p-6`}
            >
              <div className={surface.iconBox}>
                <Icon size={ICON_BOX} className="text-amber-300/80" />
              </div>
              <h3 className="mt-5 text-[15px] font-normal text-white">
                {pillar.title}
              </h3>
              <p className={`${type.bodySm} mt-2`}>{pillar.body}</p>
            </div>
          );
        })}
      </div>
    </section>
  );
}

function PersonaCard({ persona, delay }: { persona: Persona; delay: number }) {
  const Icon = persona.icon;
  return (
    <div
      data-scroll-reveal
      style={{ ["--scroll-delay" as string]: `${delay}ms` }}
      className={`group relative overflow-hidden rounded-[18px] ${surface.panel} ${surface.panelHover} ${layout.cardP}`}
    >
      <div className="flashlight-bg absolute inset-0 pointer-events-none" />
      <div className="relative flex items-start gap-5">
        <div className={surface.iconBox}>
          <Icon size={ICON_BOX} className="text-white/80" />
        </div>
        <div>
          <h3 className={type.h3}>{persona.title}</h3>
          <p className={`${type.body} mt-2`}>{persona.body}</p>
        </div>
      </div>
    </div>
  );
}
