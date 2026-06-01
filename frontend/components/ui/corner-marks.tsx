export function CornerMarks() {
  const cls =
    "hidden lg:block absolute w-2 h-2 border border-white/20 bg-[#040506] z-50";
  return (
    <>
      <div className={`${cls} -top-1 -left-1`} />
      <div className={`${cls} -top-1 -right-1`} />
      <div className={`${cls} -bottom-1 -left-1`} />
      <div className={`${cls} -bottom-1 -right-1`} />
    </>
  );
}
