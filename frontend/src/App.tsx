import { useMemo, useRef, useState } from "react";
import {
  BarChart3,
  ChevronLeft,
  Flag,
  Gauge,
  Map,
  MapPin,
  MessageCircle,
  Navigation,
  Play,
  Plus,
  RotateCcw,
  Target,
  Trophy
} from "lucide-react";

type RoundSettings = {
  course: string;
  tees: string;
  startingHole: number;
  ball: string;
  bag: string;
};

type MarkerPosition = {
  x: number;
  y: number;
};

type Recommendation = {
  club: string;
  target: string;
  risk: string;
  reason: string;
  safe: string;
  aggressive: string;
};

const sampleCourse = {
  name: "Mercury National",
  location: "Prototype Course",
  tees: ["Gold", "White", "Blue"],
  holes: [
    {
      number: 1,
      par: 4,
      yards: 421,
      name: "First Signal",
      front: 386,
      middle: 402,
      back: 417,
      fairwayCenter: 258,
      waterCarry: 233
    }
  ]
};

const carryWindows = [
  { club: "Driver", min: 265, max: 285 },
  { club: "Mini Driver", min: 240, max: 250 },
  { club: "4 iron", min: 210, max: 225 },
  { club: "5 iron", min: 195, max: 210 },
  { club: "6 iron", min: 190, max: 200 },
  { club: "7 iron", min: 175, max: 180 },
  { club: "8 iron", min: 160, max: 170 },
  { club: "9 iron", min: 140, max: 150 },
  { club: "PW", min: 130, max: 139 },
  { club: "50 degree", min: 120, max: 128 },
  { club: "54 degree", min: 105, max: 114 },
  { club: "60 degree", min: 85, max: 95 }
];

function clamp(value: number, min: number, max: number) {
  return Math.min(max, Math.max(min, value));
}

function yardageFromMarker(marker: MarkerPosition) {
  const tee = { x: 50, y: 88 };
  const green = { x: 50, y: 13 };
  const progress = clamp((tee.y - marker.y) / (tee.y - green.y), 0, 1);
  const lateralPenalty = Math.abs(marker.x - 50) * 0.9;
  return Math.round(progress * sampleCourse.holes[0].yards + lateralPenalty);
}

function getRecommendation(yards: number): Recommendation {
  if (yards >= 255) {
    return {
      club: "Mini Driver",
      target: "Fairway center, favoring the right-center start line",
      risk: "Medium",
      reason:
        "Driver adds speed but also the biggest penalty spread. Mini driver keeps the tee shot aggressive enough while matching the current trust profile.",
      safe: "4 iron to the widest fairway section",
      aggressive: "Driver only if the left hook miss has room"
    };
  }

  const match =
    carryWindows.find((club) => yards >= club.min - 4 && yards <= club.max + 6) ??
    carryWindows.reduce((best, club) => {
      const bestGap = Math.abs(yards - (best.min + best.max) / 2);
      const gap = Math.abs(yards - (club.min + club.max) / 2);
      return gap < bestGap ? club : best;
    }, carryWindows[0]);

  const wedgeNote = match.club.includes("degree")
    ? "Knockdown wedge is favored because full wedges can bring both pushes and pulls into play."
    : "Start line tends to be right, so the target should account for that instead of fighting it.";

  return {
    club: match.club,
    target: "Middle of the green or widest available landing window",
    risk: yards > 190 ? "Medium-high" : "Medium-low",
    reason: `${match.club} fits the current carry window. ${wedgeNote}`,
    safe: "Take one more club and smooth it to the fat side",
    aggressive: "Attack only if short-side miss is not costly"
  };
}

function StartRoundScreen({ onStart }: { onStart: (settings: RoundSettings) => void }) {
  const [settings, setSettings] = useState<RoundSettings>({
    course: sampleCourse.name,
    tees: "White",
    startingHole: 1,
    ball: "Maxfli Tour X",
    bag: "Current Mercury bag"
  });

  return (
    <main className="app-shell start-shell">
      <section className="brand-panel">
        <div>
          <p className="eyebrow">Mercury</p>
          <h1>Start Round</h1>
          <p className="lede">
            Load the course before the tee box, confirm the setup, then launch the on-course view.
          </p>
        </div>
        <div className="brand-mark" aria-hidden="true">
          <Navigation size={34} />
        </div>
      </section>

      <section className="setup-panel" aria-label="Round setup">
        <label>
          Course
          <select
            value={settings.course}
            onChange={(event) => setSettings({ ...settings, course: event.target.value })}
          >
            <option>{sampleCourse.name}</option>
          </select>
        </label>

        <label>
          Tees
          <select
            value={settings.tees}
            onChange={(event) => setSettings({ ...settings, tees: event.target.value })}
          >
            {sampleCourse.tees.map((tee) => (
              <option key={tee}>{tee}</option>
            ))}
          </select>
        </label>

        <label>
          Starting Hole
          <select
            value={settings.startingHole}
            onChange={(event) => setSettings({ ...settings, startingHole: Number(event.target.value) })}
          >
            <option value={1}>Hole 1</option>
            <option value={10}>Hole 10</option>
          </select>
        </label>

        <label>
          Ball
          <select
            value={settings.ball}
            onChange={(event) => setSettings({ ...settings, ball: event.target.value })}
          >
            <option>Maxfli Tour X</option>
          </select>
        </label>

        <label>
          Bag
          <select
            value={settings.bag}
            onChange={(event) => setSettings({ ...settings, bag: event.target.value })}
          >
            <option>Current Mercury bag</option>
          </select>
        </label>

        <button className="primary-action" type="button" onClick={() => onStart(settings)}>
          <Play size={18} />
          Begin Round
        </button>
      </section>

      <nav className="bottom-tabs" aria-label="Primary navigation">
        <button className="tab active" type="button">
          <Map size={18} />
          Play
        </button>
        <button className="tab" type="button">
          <Trophy size={18} />
          Rounds
        </button>
        <button className="tab" type="button">
          <BarChart3 size={18} />
          Analytics
        </button>
      </nav>
    </main>
  );
}

function HoleMap({
  marker,
  setMarker
}: {
  marker: MarkerPosition;
  setMarker: (marker: MarkerPosition) => void;
}) {
  const mapRef = useRef<HTMLDivElement | null>(null);
  const [dragging, setDragging] = useState(false);
  const yards = yardageFromMarker(marker);

  function updateMarker(clientX: number, clientY: number) {
    const map = mapRef.current;
    if (!map) return;
    const rect = map.getBoundingClientRect();
    const x = clamp(((clientX - rect.left) / rect.width) * 100, 8, 92);
    const y = clamp(((clientY - rect.top) / rect.height) * 100, 8, 92);
    setMarker({ x, y });
  }

  return (
    <div
      className="hole-map"
      ref={mapRef}
      onPointerDown={(event) => {
        setDragging(true);
        updateMarker(event.clientX, event.clientY);
      }}
      onPointerMove={(event) => {
        if (dragging) updateMarker(event.clientX, event.clientY);
      }}
      onPointerUp={() => setDragging(false)}
      onPointerCancel={() => setDragging(false)}
      role="application"
      aria-label="Interactive hole map with draggable target marker"
    >
      <div className="map-texture" />
      <div className="rough left" />
      <div className="rough right" />
      <div className="fairway" />
      <div className="green" />
      <div className="bunker bunker-left" />
      <div className="bunker bunker-right" />
      <div className="water" />
      <div className="tee-box" />

      <div className="pin-label" style={{ left: "54%", top: "11%" }}>
        <Flag size={15} />
        Back 417
      </div>

      <div className="hazard-label" style={{ left: "11%", top: "47%" }}>
        Water 233
      </div>

      <div className="position-marker" style={{ left: "50%", top: "88%" }} aria-label="Current position">
        <Navigation size={20} />
      </div>

      <div
        className="target-marker"
        style={{ left: `${marker.x}%`, top: `${marker.y}%` }}
        aria-label={`Target marker, ${yards} yards`}
      >
        <div className="yardage-bubble">{yards}y</div>
        <Target size={25} />
      </div>
    </div>
  );
}

function CaddieDialog({
  yards,
  recommendation,
  onClose
}: {
  yards: number;
  recommendation: Recommendation;
  onClose: () => void;
}) {
  return (
    <div className="dialog-backdrop" role="presentation" onClick={onClose}>
      <section className="caddie-dialog" role="dialog" aria-modal="true" aria-label="Caddie recommendation" onClick={(event) => event.stopPropagation()}>
        <div className="dialog-header">
          <div>
            <p className="eyebrow">Mercury Caddie</p>
            <h2>{yards} yards</h2>
          </div>
          <button className="icon-button" type="button" onClick={onClose} aria-label="Close caddie">
            <ChevronLeft size={22} />
          </button>
        </div>

        <div className="recommendation-main">
          <p className="label">Recommended club</p>
          <strong>{recommendation.club}</strong>
          <p>{recommendation.target}</p>
        </div>

        <div className="risk-strip">
          <Gauge size={18} />
          Risk: {recommendation.risk}
        </div>

        <p className="reason">{recommendation.reason}</p>

        <div className="option-grid">
          <div>
            <p className="label">Safer</p>
            <span>{recommendation.safe}</span>
          </div>
          <div>
            <p className="label">Aggressive</p>
            <span>{recommendation.aggressive}</span>
          </div>
        </div>
      </section>
    </div>
  );
}

function ActiveRoundScreen({
  settings,
  onReset
}: {
  settings: RoundSettings;
  onReset: () => void;
}) {
  const [marker, setMarker] = useState<MarkerPosition>({ x: 50, y: 42 });
  const [caddieOpen, setCaddieOpen] = useState(false);
  const [score, setScore] = useState(0);
  const hole = sampleCourse.holes[0];
  const yards = yardageFromMarker(marker);
  const recommendation = useMemo(() => getRecommendation(yards), [yards]);

  return (
    <main className="app-shell play-shell">
      <header className="play-header">
        <button className="icon-button" type="button" onClick={onReset} aria-label="Back to start round">
          <ChevronLeft size={22} />
        </button>
        <div>
          <p>{settings.course}</p>
          <h1>
            Hole {hole.number} <span>Par {hole.par}</span>
          </h1>
        </div>
        <button className="score-button" type="button" onClick={() => setScore(score + 1)} aria-label="Add stroke">
          <Plus size={18} />
          {score}
        </button>
      </header>

      <HoleMap marker={marker} setMarker={setMarker} />

      <section className="yardage-panel" aria-label="Current yardages">
        <div>
          <p className="label">Target</p>
          <strong>{yards}y</strong>
        </div>
        <div>
          <p className="label">Front</p>
          <strong>{hole.front}y</strong>
        </div>
        <div>
          <p className="label">Middle</p>
          <strong>{hole.middle}y</strong>
        </div>
        <div>
          <p className="label">Back</p>
          <strong>{hole.back}y</strong>
        </div>
      </section>

      <section className="round-actions" aria-label="Round actions">
        <button type="button">
          <MapPin size={18} />
          Start Shot
        </button>
        <button type="button">
          <Flag size={18} />
          Mark Result
        </button>
        <button className="caddie-action" type="button" onClick={() => setCaddieOpen(true)}>
          <MessageCircle size={18} />
          Ask Caddie
        </button>
      </section>

      <section className="course-note" aria-label="Course context">
        <p className="label">{settings.tees} tees · {settings.ball}</p>
        <p>
          Drag the target marker for carry, layup, or approach yardage. The caddie uses this target and the current player profile.
        </p>
      </section>

      <nav className="bottom-tabs" aria-label="Primary navigation">
        <button className="tab active" type="button">
          <Map size={18} />
          Play
        </button>
        <button className="tab" type="button">
          <Trophy size={18} />
          Rounds
        </button>
        <button className="tab" type="button">
          <BarChart3 size={18} />
          Analytics
        </button>
      </nav>

      {caddieOpen && <CaddieDialog yards={yards} recommendation={recommendation} onClose={() => setCaddieOpen(false)} />}
    </main>
  );
}

export default function App() {
  const [roundSettings, setRoundSettings] = useState<RoundSettings | null>(null);

  if (!roundSettings) {
    return <StartRoundScreen onStart={setRoundSettings} />;
  }

  return <ActiveRoundScreen settings={roundSettings} onReset={() => setRoundSettings(null)} />;
}
