import type { ReactNode } from "react";
import { cn } from "@/lib/cn";
import { type } from "@/lib/tokens";

export function SectionMarker({
  num,
  label,
  className,
}: {
  num: string;
  label: string;
  className?: string;
}) {
  return (
    <div className={cn(type.eyebrow, className)}>
      <span>{num}</span>
      <span className="w-6 h-px bg-white/15" aria-hidden />
      <span>{label}</span>
    </div>
  );
}

export function SectionHeading({
  marker,
  title,
  body,
  align = "left",
}: {
  marker: { num: string; label: string };
  title: readonly string[];
  body?: string;
  align?: "left" | "center";
}) {
  return (
    <div
      data-scroll-reveal="copy"
      className={cn(
        "flex flex-col gap-6",
        align === "center" && "items-center text-center",
      )}
    >
      <SectionMarker num={marker.num} label={marker.label} />
      <h2 className={cn(type.h2, "max-w-[20ch]")}>
        {title.map((line, i) => (
          <span key={i} className="block">
            {line}
          </span>
        ))}
      </h2>
      {body && (
        <p className={cn(type.body, align === "center" ? "max-w-[58ch]" : "max-w-[54ch]")}>
          {body}
        </p>
      )}
    </div>
  );
}

export function GradientPanel({
  children,
  className,
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <div
      className={cn(
        "relative rounded-[20px] p-[1px] bg-gradient-to-br from-white/12 via-white/[0.04] to-transparent",
        className,
      )}
    >
      <div className="relative h-full rounded-[19px] bg-[#0a0a0c] overflow-hidden">
        {children}
      </div>
    </div>
  );
}
