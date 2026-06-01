import type { SVGProps } from "react";
import { HugeiconsIcon, type IconSvgElement } from "@hugeicons/react";
import {
  Alert02Icon,
  ArrowDown01Icon,
  ArrowRight01Icon,
  ArrowUpRight01Icon,
  BotIcon,
  Copy01Icon,
  CpuIcon,
  GaugeIcon,
  Github01Icon,
  GridIcon,
  Layers01Icon,
  Mic01Icon,
  SlidersHorizontalIcon,
  SparklesIcon,
  ThumbsUpIcon,
  ViewIcon,
  WifiDisconnected01Icon,
} from "@hugeicons/core-free-icons";

type IconProps = { size?: number } & Omit<SVGProps<SVGSVGElement>, "strokeWidth">;

export type Icon = ((props: IconProps) => React.ReactElement) & {
  displayName?: string;
};

const wrap = (glyph: IconSvgElement, name: string): Icon => {
  const Glyph: Icon = ({ size = 18, ...rest }) => (
    <HugeiconsIcon icon={glyph} size={size} strokeWidth={1.5} {...rest} />
  );
  Glyph.displayName = name;
  return Glyph;
};

export const Eye = wrap(ViewIcon, "Eye");
export const Alert = wrap(Alert02Icon, "Alert");
export const Grid = wrap(GridIcon, "Grid");
export const Teach = wrap(ThumbsUpIcon, "Teach");
export const Chip = wrap(CpuIcon, "Chip");
export const Offline = wrap(WifiDisconnected01Icon, "Offline");
export const Tune = wrap(SlidersHorizontalIcon, "Tune");
export const Twins = wrap(Copy01Icon, "Twins");
export const Gauge = wrap(GaugeIcon, "Gauge");
export const Layers = wrap(Layers01Icon, "Layers");
export const Agent = wrap(BotIcon, "Agent");
export const Mic = wrap(Mic01Icon, "Mic");
export const Sparkles = wrap(SparklesIcon, "Sparkles");
export const ArrowDown = wrap(ArrowDown01Icon, "ArrowDown");
export const ArrowRight = wrap(ArrowRight01Icon, "ArrowRight");
export const External = wrap(ArrowUpRight01Icon, "External");
export const Github = wrap(Github01Icon, "Github");

const makeFill = (path: React.ReactNode, name: string): Icon => {
  const Glyph: Icon = ({ size = 18, ...rest }) => (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="currentColor"
      {...rest}
      aria-hidden
    >
      {path}
    </svg>
  );
  Glyph.displayName = name;
  return Glyph;
};

export const BrandQdrant = makeFill(
  <path d="m12 16.5 3.897-2.25v-4.5L12 7.5 8.103 9.75v4.5zM1.607 18 12 24l3.897-2.25v-4.5L12 19.5l-6.495-3.75v-7.5L12 4.5l6.495 3.75v15L22.393 21V6L12 0 1.607 6Z" />,
  "BrandQdrant",
);

export const BrandOpenCV = makeFill(
  <path d="M11.8992.8525C8.735.8525 6.17 3.4175 6.17 6.5817c0 2.102 1.1321 3.9398 2.8198 4.9366l1.6412-2.7849c.0411-.0699.0176-.1593-.0495-.2048-.6233-.4227-1.0328-1.137-1.0328-1.947 0-1.298 1.0524-2.3504 2.3505-2.3504 1.2981 0 2.3505 1.0524 2.3505 2.3505 0 .8098-.4095 1.5242-1.0328 1.947-.0671.0454-.0907.1348-.0495.2047l1.6414 2.785c1.6878-.9969 2.8199-2.8346 2.8199-4.9367 0-3.1642-2.5653-5.7292-5.7295-5.7292zm-6.17 10.8366C2.565 11.6891 0 14.2541 0 17.4183c0 3.1642 2.565 5.7292 5.7292 5.7292 3.1798 0 5.8074-2.6995 5.7275-5.8762H8.2313c-.0847 0-.1513.0717-.1519.1564-.0082 1.266-1.0644 2.3411-2.3502 2.3411-1.2981 0-2.3505-1.0524-2.3505-2.3505 0-1.2982 1.0524-2.3505 2.3505-2.3505.34 0 .663.0724.9547.2022.0713.0318.1566.0077.1962-.0595l1.6464-2.7935c-.8273-.4636-1.7815-.7279-2.7973-.7279zm15.4424.7614l-1.6366 2.7878c-.041.07-.0172.1594.05.2048.624.4217 1.0348 1.1354 1.0363 1.9452.0022 1.298-1.0483 2.352-2.3465 2.3542-1.298.0023-2.3523-1.0482-2.3545-2.3462-.0015-.8098.4068-1.5248 1.0294-1.9486.067-.0457.0905-.1353.0492-.2051l-1.6464-2.7818c-1.6859.9998-2.8146 2.8394-2.811 4.9415.0056 3.1641 2.575 5.7248 5.7393 5.7192 3.1641-.0054 5.7246-2.575 5.7192-5.7392-.0037-2.1022-1.139-3.938-2.8284-4.9318z" />,
  "BrandOpenCV",
);
