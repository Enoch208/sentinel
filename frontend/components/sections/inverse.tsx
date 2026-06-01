import { SectionHeading } from "@/components/ui/primitives";
import { INVERSE } from "@/lib/content";
import { layout, type } from "@/lib/tokens";

export function Inverse() {
  return (
    <section id="inverse" className={`${layout.container} ${layout.sectionX} ${layout.sectionY}`}>
      <div className="grid lg:grid-cols-[1.4fr_1fr] gap-12 lg:gap-16 items-end">
        <SectionHeading
          marker={INVERSE.marker}
          title={INVERSE.title}
          body={INVERSE.body}
        />
        <div
          data-scroll-reveal
          className="relative rounded-[20px] border border-white/[0.07] bg-[#0a0a0c] p-8 md:p-10 group overflow-hidden"
        >
          <div className="flashlight-bg absolute inset-0 pointer-events-none" />
          <div className="relative">
            <div className="[font-family:var(--font-display)] text-5xl md:text-6xl font-extralight tracking-tight text-amber-300/90">
              {INVERSE.stat}
            </div>
            <p className={`${type.bodySm} mt-3 max-w-[28ch]`}>
              {INVERSE.statLabel}
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
