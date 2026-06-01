import { Cta } from "@/components/sections/cta";
import { Dossier } from "@/components/sections/dossier";
import { Engine } from "@/components/sections/engine";
import { Footer } from "@/components/sections/footer";
import { Hero } from "@/components/sections/hero";
import { Inverse } from "@/components/sections/inverse";
import { Loop } from "@/components/sections/loop";
import { Sponsors } from "@/components/sections/sponsors";
import { Who } from "@/components/sections/who";

export default function Home() {
  return (
    <>
      <Hero />
      <Sponsors />
      <Inverse />
      <Loop />
      <Engine />
      <Dossier />
      <Who />
      <Cta />
      <Footer />
    </>
  );
}
