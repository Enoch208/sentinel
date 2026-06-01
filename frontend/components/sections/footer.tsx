import Image from "next/image";
import { BRAND, FOOTER } from "@/lib/content";
import { layout, type } from "@/lib/tokens";

export function Footer() {
  return (
    <footer className={`${layout.containerWide} ${layout.sectionX} pb-12`}>
      <div className="rounded-[20px] border border-white/[0.07] bg-[#0a0a0c] p-8 md:p-12">
        <div className="grid gap-10 md:grid-cols-[1.4fr_repeat(3,1fr)]">
          <div>
            <div className="flex items-center gap-2.5">
              <Image
                src="/logo.png"
                alt="Sentinel"
                width={26}
                height={26}
                className="mix-blend-screen"
              />
              <span className="[font-family:var(--font-display)] text-[15px] font-light tracking-tight">
                {BRAND.name}
              </span>
            </div>
            <p className={`${type.bodySm} mt-4 max-w-[32ch]`}>{BRAND.tagline}</p>
            <p className="mt-4 font-mono text-[11px] text-white/35">
              {BRAND.builtWith}
            </p>
          </div>

          {FOOTER.links.map((col) => (
            <div key={col.heading}>
              <h4 className="font-mono text-[11px] uppercase tracking-[0.22em] text-white/40">
                {col.heading}
              </h4>
              <ul className="mt-4 space-y-2.5">
                {col.items.map((item) => (
                  <li key={item.label}>
                    <a
                      href={item.href}
                      className="text-[13px] font-light text-white/55 hover:text-white transition-colors"
                    >
                      {item.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-12 pt-6 border-t border-white/[0.07] flex flex-col sm:flex-row items-center justify-between gap-3">
          <span className="font-mono text-[11px] uppercase tracking-[0.18em] text-white/35">
            {FOOTER.hackathon.label}
          </span>
          <span className="font-mono text-[11px] uppercase tracking-[0.18em] text-white/35">
            {FOOTER.hackathon.deadline}
          </span>
        </div>
      </div>
    </footer>
  );
}
