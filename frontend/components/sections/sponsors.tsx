import { SPONSORS } from "@/lib/content";
import { External } from "@/lib/icons";
import { layout } from "@/lib/tokens";

export function Sponsors() {
  return (
    <section className={`${layout.container} ${layout.sectionX} pt-16 md:pt-20`}>
      <div
        data-scroll-reveal
        className="flex flex-col items-center text-center gap-8"
      >
        <span className="font-mono text-[11px] uppercase tracking-[0.22em] text-white/40">
          {SPONSORS.eyebrow}
        </span>

        <div className="flex flex-wrap items-center justify-center gap-x-10 gap-y-6 md:gap-x-14">
          {(() => {
            const Logo = SPONSORS.primary.logo;
            return (
              <a
                href={SPONSORS.primary.href}
                target="_blank"
                rel="noreferrer"
                className="group flex items-center gap-3"
              >
                {Logo && <Logo size={26} className="text-amber-300/90" />}
                <span className="flex flex-col items-start leading-tight">
                  <span className="[font-family:var(--font-display)] text-xl font-light text-white transition-colors">
                    {SPONSORS.primary.name}
                  </span>
                  <span className="font-mono text-[10px] uppercase tracking-[0.16em] text-white/40">
                    {SPONSORS.primary.role}
                  </span>
                </span>
                <External
                  size={14}
                  className="text-white/25 group-hover:text-white/60 transition-colors"
                />
              </a>
            );
          })()}

          <span className="hidden md:block h-8 w-px bg-white/10" aria-hidden />

          {SPONSORS.items.map((s) => {
            const Logo = s.logo;
            return (
              <a
                key={s.name}
                href={s.href}
                target="_blank"
                rel="noreferrer"
                className="group flex items-center gap-2.5"
              >
                {Logo && (
                  <Logo
                    size={18}
                    className="text-white/45 group-hover:text-white/80 transition-colors"
                  />
                )}
                <span className="flex flex-col items-start leading-tight">
                  <span className="[font-family:var(--font-display)] text-base font-light text-white/70 group-hover:text-white transition-colors">
                    {s.name}
                  </span>
                  <span className="font-mono text-[10px] uppercase tracking-[0.16em] text-white/35">
                    {s.role}
                  </span>
                </span>
              </a>
            );
          })}
        </div>
      </div>
    </section>
  );
}
