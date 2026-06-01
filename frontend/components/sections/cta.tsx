import { PerceptionField } from "@/components/ui/perception-field";
import { SectionMarker } from "@/components/ui/primitives";
import { CTA } from "@/lib/content";
import { ArrowRight, External } from "@/lib/icons";
import { layout, type } from "@/lib/tokens";

export function Cta() {
  return (
    <section className={`${layout.containerWide} ${layout.sectionX} pb-8`}>
      <div className="relative rounded-[28px] p-[1px] bg-gradient-to-br from-white/15 via-white/[0.04] to-transparent overflow-hidden">
        <div className="relative rounded-[27px] bg-[#08080a] overflow-hidden">
          <div className="absolute inset-0 opacity-30 pointer-events-none">
            <PerceptionField cols={14} rows={8} anomaly={52} className="p-10" />
          </div>
          <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(ellipse_at_50%_50%,rgba(8,8,10,0.5)_0%,rgba(8,8,10,0.95)_75%)]" />

          <div className="relative px-6 py-24 md:px-16 md:py-32 flex flex-col items-center text-center">
            <SectionMarker num={CTA.marker.num} label={CTA.marker.label} />
            <h2 className={`${type.h2} mt-6 max-w-[20ch] reveal`}>
              {CTA.title.map((line, i) => (
                <span key={i} className="block">
                  {line}
                </span>
              ))}
            </h2>
            <p className={`${type.body} mt-6 max-w-[56ch]`}>{CTA.body}</p>

            <div className="mt-10 flex flex-col sm:flex-row items-center gap-3">
              <a
                href={CTA.primary.href}
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center gap-2 rounded-full bg-white px-6 py-3 text-[14px] font-medium text-black hover:bg-white/90 transition-colors"
              >
                {CTA.primary.label}
                <External size={16} />
              </a>
              <a
                href={CTA.secondary.href}
                className="inline-flex items-center gap-2 rounded-full border border-white/15 bg-white/[0.04] px-6 py-3 text-[14px] font-light text-white/80 hover:border-white/30 hover:text-white transition-colors"
              >
                {CTA.secondary.label}
                <ArrowRight size={16} />
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
