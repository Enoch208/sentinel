import Image from "next/image";
import { cn } from "@/lib/cn";
import { BRAND, NAV_LINKS } from "@/lib/content";
import { Github } from "@/lib/icons";

export function Nav() {
  return (
    <nav className="flex items-center justify-between w-full">
      <a href="#top" className="flex items-center gap-2.5 group">
        <Image
          src="/logo.png"
          alt="Sentinel"
          width={28}
          height={28}
          priority
          className="mix-blend-screen"
        />
        <span className="[font-family:var(--font-display)] text-[15px] font-light tracking-tight text-white">
          {BRAND.name}
        </span>
      </a>

      <div className="hidden md:flex items-center gap-8">
        {NAV_LINKS.map((l) => (
          <a
            key={l.href}
            href={l.href}
            className="text-[13px] font-light text-white/55 hover:text-white transition-colors"
          >
            {l.label}
          </a>
        ))}
      </div>

      <a
        href={BRAND.github}
        target="_blank"
        rel="noreferrer"
        className={cn(
          "inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.04]",
          "px-3.5 py-1.5 text-[12px] font-light text-white/80 hover:border-white/20 hover:text-white transition-colors",
        )}
      >
        <Github size={15} />
        GitHub
      </a>
    </nav>
  );
}
