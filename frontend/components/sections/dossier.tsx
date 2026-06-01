import { SectionHeading } from "@/components/ui/primitives";
import { DOSSIER } from "@/lib/content";
import { layout, type } from "@/lib/tokens";

export function Dossier() {
  return (
    <section
      id="proof"
      className={`${layout.container} ${layout.sectionX} ${layout.sectionYTight}`}
    >
      <div className="grid lg:grid-cols-[1fr_1.1fr] gap-12 lg:gap-16 items-center">
        <SectionHeading
          marker={DOSSIER.marker}
          title={DOSSIER.title}
          body={DOSSIER.body}
        />

        <div
          data-scroll-reveal
          className="grid grid-cols-2 gap-px rounded-[20px] border border-white/[0.07] bg-white/[0.06] overflow-hidden"
        >
          {DOSSIER.metrics.map((m) => (
            <div key={m.label} className="bg-[#0a0a0c] p-7 md:p-9">
              <div className="[font-family:var(--font-display)] text-3xl md:text-4xl font-extralight tracking-tight text-white">
                {m.value}
              </div>
              <p className={`${type.bodySm} mt-2`}>{m.label}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
