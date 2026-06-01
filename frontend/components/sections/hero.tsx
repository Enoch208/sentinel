import { DarkVeil } from "@/components/dark-veil";
import { Nav } from "@/components/sections/nav";
import { CornerMarks } from "@/components/ui/corner-marks";
import { PerceptionField } from "@/components/ui/perception-field";
import { SectionMarker } from "@/components/ui/primitives";
import { HERO } from "@/lib/content";
import { ArrowDown, ArrowRight } from "@/lib/icons";
import { type } from "@/lib/tokens";

export function Hero() {
  return (
    <section
      id="top"
      className="relative w-full max-w-[1440px] mx-auto lg:px-8 lg:py-8"
    >
      <CornerMarks />

      <div className="relative lg:rounded-[28px] overflow-hidden p-0 lg:p-[1px] bg-gradient-to-br from-white/15 via-white/[0.04] to-transparent">
        <div className="absolute inset-0 lg:inset-[1px] bg-[#08080a] lg:rounded-[27px]" />
        <div className="absolute inset-0 lg:inset-[1px] overflow-hidden lg:rounded-[27px]">
          <DarkVeil className="opacity-[0.55]" />
        </div>
        <div className="absolute inset-0 lg:inset-[1px] lg:rounded-[27px] pointer-events-none bg-[radial-gradient(ellipse_at_50%_18%,rgba(20,20,24,0)_0%,rgba(4,5,6,0.62)_58%,rgba(4,5,6,0.94)_100%)]" />

        <div className="relative flex flex-col w-full px-6 py-7 md:px-10 md:py-10 min-h-[760px]">
          <Nav />

          <main className="flex-1 flex flex-col items-center text-center w-full mt-12 md:mt-16">
            <div className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.04] px-3 py-1 mb-8 reveal backdrop-blur-md">
              <span className="h-1.5 w-1.5 rounded-full bg-amber-300 shadow-[0_0_8px_rgba(252,211,77,0.85)]" />
              <span className="text-[11px] uppercase tracking-[0.22em] text-white/70 font-mono">
                {HERO.badge}
              </span>
            </div>

            <h1 className={`${type.h1} mb-5 max-w-[900px] mx-auto reveal`}>
              {HERO.headline.map((line, i) => (
                <span key={i} className="block">
                  {line}
                </span>
              ))}
            </h1>

            <p className={`${type.body} max-w-[560px] mx-auto mb-10 reveal`}>
              {HERO.sub}
            </p>

            <div className="relative w-full max-w-[640px] mx-auto reveal">
              <PerceptionField />
            </div>
          </main>

          <footer className="flex items-center justify-between w-full mt-12 md:mt-10">
            <SectionMarker num={HERO.marker.num} label={HERO.marker.label} />
            <a
              href="#inverse"
              className="hidden md:inline-flex items-center gap-2 text-[11px] uppercase tracking-[0.22em] text-white/50 hover:text-white/80 font-mono transition-colors"
            >
              The inverse of search
              <ArrowDown size={12} />
            </a>
            <a
              href="#loop"
              className="md:hidden inline-flex items-center gap-2 text-[11px] uppercase tracking-[0.22em] text-white/50 font-mono"
            >
              The loop <ArrowRight size={12} />
            </a>
          </footer>
        </div>
      </div>
    </section>
  );
}
