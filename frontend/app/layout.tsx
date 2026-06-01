import type { Metadata } from "next";
import { DM_Sans, Inter, JetBrains_Mono } from "next/font/google";
import { ScrollReveal } from "@/components/scroll-reveal";
import { Backdrop } from "@/components/ui/backdrop";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-sans",
  weight: ["200", "300", "400", "500"],
});

const dmSans = DM_Sans({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-display",
  weight: ["200", "300", "400"],
});

const jetbrains = JetBrains_Mono({
  subsets: ["latin"],
  display: "swap",
  variable: "--font-mono",
  weight: ["400", "500"],
});

const TITLE = "Sentinel — Notice what doesn't belong";
const DESCRIPTION =
  "Sentinel is an on-device, fully-offline perceptual instrument. It learns the normal of a space with embedded Qdrant and flags the out-of-place in real time. No query box. No chatbot. No cloud.";

export const metadata: Metadata = {
  title: TITLE,
  description: DESCRIPTION,
  metadataBase: new URL("https://sentinel.local"),
  icons: { icon: "/logo.png", apple: "/logo.png" },
  openGraph: {
    title: TITLE,
    description: DESCRIPTION,
    images: [{ url: "/logo.png", width: 1254, height: 1254, alt: "Sentinel" }],
  },
  twitter: {
    card: "summary_large_image",
    title: TITLE,
    description: DESCRIPTION,
    images: ["/logo.png"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html
      lang="en"
      className={`${inter.variable} ${dmSans.variable} ${jetbrains.variable} h-full antialiased`}
    >
      <body className="min-h-full bg-[#040506] text-white font-sans font-extralight selection:bg-amber-300/25 selection:text-white overflow-x-hidden">
        <Backdrop />
        <ScrollReveal />
        {children}
      </body>
    </html>
  );
}
