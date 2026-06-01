export const layout = {
  container: "max-w-[1240px] mx-auto",
  containerWide: "max-w-[1440px] mx-auto",
  sectionX: "px-6 md:px-10",
  sectionY: "py-28 md:py-36",
  sectionYTight: "py-20 md:py-24",
  cardP: "p-7 md:p-9",
  cardPLg: "p-8 md:p-12",
  gridGap: "gap-5 md:gap-6",
} as const;

export const type = {
  h1: "[font-family:var(--font-display)] text-[44px] sm:text-6xl lg:text-[80px] leading-[0.98] tracking-[-0.035em] font-extralight text-white",
  h2: "[font-family:var(--font-display)] text-3xl md:text-5xl lg:text-[56px] leading-[1.02] tracking-[-0.025em] font-extralight text-white",
  h3: "[font-family:var(--font-display)] text-xl md:text-2xl leading-tight tracking-[-0.015em] font-light text-white",
  eyebrow:
    "inline-flex items-center gap-2 text-[11px] uppercase tracking-[0.22em] text-white/45 font-mono",
  body: "text-[15px] md:text-base text-white/55 font-extralight leading-[1.7]",
  bodySm: "text-[13px] text-white/45 font-extralight leading-[1.65]",
  mono: "font-mono text-[12px] text-white/40 tracking-wide",
} as const;

export const surface = {
  panel: "bg-[#0a0a0c] border border-white/[0.07]",
  panelHover:
    "hover:border-white/15 hover:bg-[#0d0d10] transition-colors duration-200",
  border: "border-white/[0.07]",
  iconBox:
    "flex h-9 w-9 shrink-0 items-center justify-center rounded-[10px] border border-white/[0.08] bg-white/[0.04]",
  glow: "shadow-[0_30px_80px_-30px_rgba(0,0,0,0.8)]",
} as const;

export const accent = {
  text: "text-amber-300/90",
  dot: "bg-amber-300 shadow-[0_0_10px_rgba(252,211,77,0.85)]",
  ring: "ring-1 ring-amber-300/40",
  calmDot: "bg-white/25",
} as const;

export const motion = {
  reveal: "reveal",
  ease: "transition-colors duration-200",
} as const;

export const ICON_INLINE = 18;
export const ICON_BOX = 16;
