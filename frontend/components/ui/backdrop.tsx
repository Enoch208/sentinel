export function Backdrop() {
  return (
    <div aria-hidden className="pointer-events-none fixed inset-0 -z-10 overflow-hidden">
      <div
        className="absolute inset-0 opacity-[0.5]"
        style={{
          backgroundImage:
            "radial-gradient(circle at center, rgba(255,255,255,0.06) 1px, transparent 1px)",
          backgroundSize: "30px 30px",
          maskImage:
            "radial-gradient(ellipse 80% 60% at 50% 0%, black 0%, transparent 70%)",
          WebkitMaskImage:
            "radial-gradient(ellipse 80% 60% at 50% 0%, black 0%, transparent 70%)",
        }}
      />
      <div
        className="absolute -top-[20%] left-1/2 h-[60vh] w-[90vw] -translate-x-1/2 rounded-full blur-[120px]"
        style={{ background: "radial-gradient(circle, rgba(45,212,191,0.07), transparent 70%)" }}
      />
      <div
        className="absolute bottom-[8%] right-[6%] h-[36vh] w-[36vw] rounded-full blur-[130px]"
        style={{ background: "radial-gradient(circle, rgba(252,211,77,0.05), transparent 70%)" }}
      />
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_50%_40%,transparent_30%,rgba(4,5,6,0.6)_100%)]" />
    </div>
  );
}
