import { SectionHeading } from "@/components/ui/primitives";
import { DOSSIER, PROOF_LINES } from "@/lib/content";
import { layout, type } from "@/lib/tokens";

const TONE: Record<string, string> = {
  dim: "text-white/35",
  normal: "text-white/65",
  flag: "text-amber-300",
  ok: "text-emerald-300/90",
};

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

        <div className="flex flex-col gap-5">
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

          <div
            data-scroll-reveal
            className="rounded-[16px] border border-white/[0.07] bg-[#08080a] overflow-hidden"
          >
            <div className="flex items-center gap-1.5 px-4 py-2.5 border-b border-white/[0.06]">
              <span className="h-2.5 w-2.5 rounded-full bg-white/15" />
              <span className="h-2.5 w-2.5 rounded-full bg-white/15" />
              <span className="h-2.5 w-2.5 rounded-full bg-amber-300/70" />
              <span className="ml-2 font-mono text-[11px] uppercase tracking-[0.18em] text-white/30">
                engine · offline
              </span>
            </div>
            <pre className="px-4 py-4 font-mono text-[12px] leading-[1.7] overflow-x-auto">
              {PROOF_LINES.map((line, i) => (
                <div key={i} className={TONE[line.tone]}>
                  {line.text}
                </div>
              ))}
            </pre>
          </div>
        </div>
      </div>
    </section>
  );
}
