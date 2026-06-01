import {
  Agent,
  Alert,
  BrandOpenCV,
  BrandQdrant,
  Chip,
  Eye,
  Gauge,
  Grid,
  Layers,
  Mic,
  Offline,
  Sparkles,
  Teach,
  Tune,
  Twins,
  type Icon,
} from "@/lib/icons";

export const BRAND = {
  name: "Sentinel",
  tagline: "It learns what belongs, and notices what doesn't.",
  github: "https://github.com/Enoch208/sentinel",
  builtWith: "Embedded Qdrant · architected for Qdrant Edge",
} as const;

export const NAV_LINKS = [
  { label: "The loop", href: "#loop" },
  { label: "Engine", href: "#engine" },
  { label: "Who it's for", href: "#who" },
] as const;

export const HERO = {
  marker: { num: "01", label: "Concept" },
  badge: "Offline · on-device · no query box",
  headline: ["Notice what", "doesn't belong."],
  sub: "Sentinel rides a camera, learns the normal of a space on-device, and flags the out-of-place in real time. No search box. No chatbot. No cloud.",
} as const;

export type Sponsor = {
  name: string;
  role: string;
  href: string;
  logo?: Icon;
};

export const SPONSORS: {
  eyebrow: string;
  primary: Sponsor;
  items: Sponsor[];
} = {
  eyebrow: "Built for the Qdrant hackathon · powered by an on-device stack",
  primary: {
    name: "Qdrant",
    role: "Vector engine · embedded & Edge",
    href: "https://qdrant.tech",
    logo: BrandQdrant,
  },
  items: [
    { name: "Qdrant Edge", role: "on-device · private beta", href: "https://qdrant.tech", logo: BrandQdrant },
    { name: "FastEmbed", role: "image embeddings", href: "https://github.com/qdrant/fastembed" },
    { name: "MobileCLIP", role: "perception model", href: "https://github.com/apple/ml-mobileclip" },
    { name: "OpenCV", role: "frame capture", href: "https://opencv.org", logo: BrandOpenCV },
  ],
};

export const INVERSE = {
  marker: { num: "02", label: "The inverse of search" },
  title: ["You can't search for", "what you didn't expect."],
  body:
    "Most edge perception answers “where is the thing I'm looking for?” The harder question in the physical world is the inverse — “what here is new, or out of place?” That's what an inspector, a guard, a lab tech is actually asking, and search can't answer it, because you can't query for the thing you didn't know to look for.",
  stat: "~1s",
  statLabel: "From out-of-place object to live flag",
} as const;

export const LOOP_INTRO = {
  marker: { num: "03", label: "The loop" },
  title: ["Watch. Teach. Explore.", "Never type."],
  body:
    "Every interaction is a gesture, never a query. Point the camera, let Sentinel learn the scene, and it flags what breaks the pattern. Tap a flag to see why and its visual twins. Nudge it 👍/👎 to tune what counts as normal.",
} as const;

export type LoopCard = {
  icon: Icon;
  step: string;
  title: string;
  blurb: string;
  variant: "field" | "flag" | "twins";
};

export const LOOP_CARDS: LoopCard[] = [
  {
    icon: Eye,
    step: "Watch",
    title: "Learn the normal",
    blurb:
      "Webcam frames are perceptually de-duplicated, embedded on-device with a small CLIP model, and upserted into a private vector memory. A rolling model of “normal” forms in seconds.",
    variant: "field",
  },
  {
    icon: Alert,
    step: "Flag",
    title: "Surface the anomaly",
    blurb:
      "Each new frame queries that memory. When its nearest neighbour falls below a learned threshold, it's far from everything seen so far — Sentinel raises a calm, self-explanatory ⚠ out-of-place flag.",
    variant: "flag",
  },
  {
    icon: Twins,
    step: "Inspect",
    title: "Why, and what's like it",
    blurb:
      "Tap a flag for its nearest “normal” memories — the why — and its visual twins, matched by how things look. Then teach with 👍 expected / 👎 anomaly to reshape the threshold.",
    variant: "twins",
  },
];

export const ENGINE_INTRO = {
  marker: { num: "04", label: "Engine" },
  title: ["One vector engine,", "running on the device."],
  body:
    "Qdrant runs in-process and fully offline — built on the client's local mode, architected to swap onto Qdrant Edge's EdgeShard when beta access lands, no code change to the query path. The whole instrument is one engine, end to end.",
} as const;

export type EngineRow = {
  icon: Icon;
  capability: string;
  use: string;
  note: string;
};

export const ENGINE_ROWS: EngineRow[] = [
  {
    icon: Eye,
    capability: "Nearest-neighbour query",
    use: "Per-frame anomaly check against the rolling “normal”, and the visual-twins lookup. Top score below threshold ⇒ flag.",
    note: "the hero loop",
  },
  {
    icon: Grid,
    capability: "Facet",
    use: "Per-zone review — tag frames by area (bench, shelf, panel) and count anomalies where they happened.",
    note: "zones",
  },
  {
    icon: Teach,
    capability: "Recommend",
    use: "Example-based retrieval behind teach-by-example — 👍/👎 become positive and negative targets.",
    note: "tactile, not typed",
  },
  {
    icon: Twins,
    capability: "Scroll → on-device PCA",
    use: "Projects the whole memory to a 2D map so you can browse clusters, with anomalies highlighted.",
    note: "explore canvas",
  },
  {
    icon: Layers,
    capability: "Scalar quantization",
    use: "Configured on the collection for a small footprint on the edge; reported honestly (active on Edge, off in local mode).",
    note: "edge-shaped",
  },
];

export const DOSSIER = {
  marker: { num: "05", label: "Proof" },
  title: ["Honest numbers,", "from the running engine."],
  body:
    "Edge is about resource constraints, so the proof is the product. Every figure is read live from the in-process engine — never hardcoded — and shown with its trade-offs.",
  metrics: [
    { value: "1.00", label: "Precision & recall on the staged scene" },
    { value: "5", label: "Qdrant capabilities on the call path" },
    { value: "2", label: "Senses — camera and microphone" },
    { value: "0", label: "Bytes that leave the device" },
  ],
} as const;

export const PROOF_LINES: { text: string; tone: "dim" | "normal" | "flag" | "ok" }[] = [
  { text: "$ uv run sentinel --synthetic", tone: "dim" },
  { text: "frame  12   learning normal…", tone: "dim" },
  { text: "frame  20   normal             score=0.998", tone: "normal" },
  { text: "frame  24   ⚠ OUT OF PLACE    score=0.852 < 0.946", tone: "flag" },
  { text: "frame  27   normal             score=0.998", tone: "normal" },
  { text: "$ uv run sentinel-eval", tone: "dim" },
  { text: "precision 1.000 · recall 1.000 · f1 1.000", tone: "ok" },
] as const;

export const WHO_MARKER = { num: "06", label: "Who it's for" } as const;

export type Persona = {
  icon: Icon;
  title: string;
  body: string;
};

export const PERSONAS: Persona[] = [
  {
    icon: Eye,
    title: "Site & safety inspection",
    body: "Walk a site and be alerted the moment something is out of place or unsafe — on air-gapped floors where you can't query for unknown hazards.",
  },
  {
    icon: Alert,
    title: "Security & facilities",
    body: "Notice when something appears that shouldn't be here. Retrieval needs a known target; novelty is the whole point.",
  },
  {
    icon: Chip,
    title: "Lab & equipment",
    body: "Flag abnormal equipment states in real time, locally — latency, privacy, and intermittent networks rule out cloud round-trips.",
  },
  {
    icon: Grid,
    title: "Retail & inventory",
    body: "Spot shelf gaps and misplaced items as you walk the aisle. Keyword search can't describe “looks wrong.”",
  },
];

export const PILLARS = [
  {
    icon: Offline,
    title: "Offline is the feature",
    body: "Kill the wifi mid-demo and nothing changes. If it needed the network, it would be wrong.",
  },
  {
    icon: Tune,
    title: "You shape it by example",
    body: "A sensitivity slider and 👍/👎 teaching — the memory adapts to your space, no configuration language.",
  },
  {
    icon: Gauge,
    title: "Auditable by default",
    body: "Every flag, teach, and exploration is recorded as an ordered, exportable session you can replay.",
  },
  {
    icon: Mic,
    title: "Multimodal on the edge",
    body: "Out-of-place sounds, not just sights — the same vector loop runs over a microphone to flag abnormal noise.",
  },
  {
    icon: Agent,
    title: "A watcher, not a bot",
    body: "An agent clusters recurring anomalies and writes an end-of-walk report. Agentic — never conversational.",
  },
  {
    icon: Sparkles,
    title: "Tunes itself for the device",
    body: "On launch it picks quantization, frame-skip, and HNSW for the hardware it's on — with a stated rationale.",
  },
] as const;

export const CTA = {
  marker: { num: "07", label: "See it" },
  title: ["Point it at a room.", "It already knows what's off."],
  body:
    "Pre-stage a normal scene, let Sentinel learn it, introduce something out of place — and watch it flag the thing you never told it to look for. Fully on-device, built for Qdrant Edge.",
  primary: {
    label: "Download for macOS",
    href: `${BRAND.github}/releases/latest`,
  },
  secondary: { label: "View on GitHub", href: BRAND.github },
  note: "Apple Silicon · fully offline · unsigned — if macOS says “damaged”, the release notes have the one-line fix to open it.",
} as const;

export const FOOTER = {
  links: [
    {
      heading: "Product",
      items: [
        { label: "The loop", href: "#loop" },
        { label: "Engine", href: "#engine" },
        { label: "Proof", href: "#proof" },
        { label: "Who it's for", href: "#who" },
      ],
    },
    {
      heading: "Repository",
      items: [{ label: "GitHub", href: BRAND.github }],
    },
    {
      heading: "Built with",
      items: [
        { label: "Qdrant", href: "https://qdrant.tech" },
        { label: "Qdrant Edge", href: "https://qdrant.tech" },
        { label: "FastEmbed", href: "https://github.com/qdrant/fastembed" },
        { label: "OpenCV", href: "https://opencv.org" },
      ],
    },
  ],
  hackathon: {
    label: "Qdrant · Think Outside the Bot",
    deadline: "Vector Space Day · SF",
  },
} as const;
