"use client";

import { useState, useRef, useEffect, useCallback } from "react";

// ─── Types ────────────────────────────────────────────────────────────────────
type Tool = "pen" | "eraser" | "highlighter" | "shape" | "text" | "select";
type Shape = "rect" | "circle" | "arrow" | "line";
type ViewMode = "gallery" | "spotlight" | "whiteboard";
type Tab = "participants" | "chat" | "settings";

interface Participant {
  id: string;
  name: string;
  role: "host" | "co-host" | "participant";
  isMuted: boolean;
  isCameraOff: boolean;
  isHandRaised: boolean;
  avatar: string;
  isActive: boolean;
}

interface ChatMessage {
  id: string;
  sender: string;
  text: string;
  time: string;
  isMe: boolean;
}

interface DrawPath {
  id: string;
  tool: Tool;
  color: string;
  size: number;
  points: { x: number; y: number }[];
  opacity: number;
}

// ─── Constants ────────────────────────────────────────────────────────────────
const PEN_COLORS = [
  "#FF3B5C", "#FF9500", "#FFD60A", "#34C759",
  "#00C7BE", "#007AFF", "#5856D6", "#FF2D55",
  "#FFFFFF", "#1C1C1E",
];

const INITIAL_PARTICIPANTS: Participant[] = [
  { id: "1", name: "You (Host)", role: "host", isMuted: false, isCameraOff: false, isHandRaised: false, avatar: "YH", isActive: true },
  { id: "2", name: "Sarah Chen", role: "co-host", isMuted: false, isCameraOff: false, isHandRaised: false, avatar: "SC", isActive: false },
  { id: "3", name: "Marcus Webb", role: "participant", isMuted: true, isCameraOff: false, isHandRaised: true, avatar: "MW", isActive: false },
  { id: "4", name: "Priya Sharma", role: "participant", isMuted: false, isCameraOff: true, isHandRaised: false, avatar: "PS", isActive: false },
  { id: "5", name: "James O'Brien", role: "participant", isMuted: true, isCameraOff: true, isHandRaised: false, avatar: "JO", isActive: false },
  { id: "6", name: "Luna Park", role: "participant", isMuted: false, isCameraOff: false, isHandRaised: false, avatar: "LP", isActive: false },
];

const INITIAL_MESSAGES: ChatMessage[] = [
  { id: "1", sender: "Sarah Chen", text: "Let's start with the Q3 review slides.", time: "10:02", isMe: false },
  { id: "2", sender: "You", text: "Sure! I'll share my screen in a moment.", time: "10:03", isMe: true },
  { id: "3", sender: "Marcus Webb", text: "Can everyone see the whiteboard now?", time: "10:04", isMe: false },
];

// ─── Sub Components ───────────────────────────────────────────────────────────
function ParticipantCard({ p, isHost }: { p: Participant; isHost: boolean }) {
  const colors: Record<Participant["role"], string> = {
    host: "#FF3B5C",
    "co-host": "#FF9500",
    participant: "#007AFF",
  };
  return (
    <div className="flex items-center gap-3 px-3 py-2 rounded-xl hover:bg-white/5 transition-colors group">
      <div
        className="w-9 h-9 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0 relative"
        style={{ background: `${colors[p.role]}22`, border: `1.5px solid ${colors[p.role]}55`, color: colors[p.role] }}
      >
        {p.avatar}
        {p.isActive && (
          <span className="absolute -bottom-0.5 -right-0.5 w-2.5 h-2.5 rounded-full bg-emerald-400 border-2 border-[#0D0D14]" />
        )}
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-1.5">
          <span className="text-sm text-white/90 font-medium truncate">{p.name}</span>
          {p.isHandRaised && <span className="text-xs">✋</span>}
        </div>
        <span className="text-xs capitalize" style={{ color: colors[p.role] }}>{p.role}</span>
      </div>
      <div className="flex gap-1.5 opacity-0 group-hover:opacity-100 transition-opacity">
        <button className="p-1 rounded-lg hover:bg-white/10 text-white/50 hover:text-white transition-colors text-xs">
          {p.isMuted ? "🔇" : "🎤"}
        </button>
        {isHost && p.id !== "1" && (
          <button className="p-1 rounded-lg hover:bg-red-500/20 text-white/50 hover:text-red-400 transition-colors text-xs">✕</button>
        )}
      </div>
    </div>
  );
}

function VideoTile({ p, large = false }: { p: Participant; large?: boolean }) {
  const colors: Record<string, string> = { SC: "#FF9500", MW: "#5856D6", PS: "#34C759", JO: "#FF2D55", LP: "#00C7BE", YH: "#007AFF" };
  return (
    <div className={`relative rounded-2xl overflow-hidden bg-[#161622] border border-white/5 ${large ? "aspect-video" : "aspect-video"}`}>
      {p.isCameraOff ? (
        <div className="absolute inset-0 flex flex-col items-center justify-center gap-2"
          style={{ background: `radial-gradient(circle at 50% 40%, ${colors[p.avatar] || "#007AFF"}22, transparent 70%)` }}>
          <div className="w-14 h-14 rounded-full flex items-center justify-center text-lg font-bold"
            style={{ background: `${colors[p.avatar] || "#007AFF"}33`, color: colors[p.avatar] || "#007AFF", border: `2px solid ${colors[p.avatar] || "#007AFF"}55` }}>
            {p.avatar}
          </div>
          <span className="text-xs text-white/40">Camera off</span>
        </div>
      ) : (
        <div className="absolute inset-0 flex items-center justify-center"
          style={{ background: `linear-gradient(135deg, ${colors[p.avatar] || "#007AFF"}15, #161622 60%)` }}>
          <div className="w-16 h-16 rounded-full flex items-center justify-center text-xl font-bold"
            style={{ background: `${colors[p.avatar] || "#007AFF"}44`, color: colors[p.avatar] || "#007AFF" }}>
            {p.avatar}
          </div>
        </div>
      )}
      {/* Name bar */}
      <div className="absolute bottom-0 left-0 right-0 px-2.5 py-1.5 bg-gradient-to-t from-black/60 to-transparent flex items-center gap-1.5">
        {p.isActive && <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />}
        <span className="text-xs text-white/90 font-medium truncate flex-1">{p.name}</span>
        {p.isMuted && <span className="text-xs opacity-60">🔇</span>}
        {p.isHandRaised && <span className="text-xs">✋</span>}
      </div>
      {p.role === "host" && (
        <div className="absolute top-2 left-2 px-1.5 py-0.5 rounded-md text-[10px] font-bold bg-[#FF3B5C]/80 text-white">HOST</div>
      )}
    </div>
  );
}

// ─── Whiteboard ───────────────────────────────────────────────────────────────
function Whiteboard({ activeTool, activeColor, penSize, onBack }: {
  activeTool: Tool; activeColor: string; penSize: number; onBack: () => void;
}) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [paths, setPaths] = useState<DrawPath[]>([]);
  const [currentPath, setCurrentPath] = useState<DrawPath | null>(null);
  const [history, setHistory] = useState<DrawPath[][]>([[]]);
  const [historyIdx, setHistoryIdx] = useState(0);

  const getPos = (e: React.MouseEvent | React.TouchEvent) => {
    const canvas = canvasRef.current!;
    const rect = canvas.getBoundingClientRect();
    const clientX = "touches" in e ? e.touches[0].clientX : e.clientX;
    const clientY = "touches" in e ? e.touches[0].clientY : e.clientY;
    return {
      x: (clientX - rect.left) * (canvas.width / rect.width),
      y: (clientY - rect.top) * (canvas.height / rect.height),
    };
  };

  const redraw = useCallback((ps: DrawPath[]) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d")!;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ps.forEach(path => {
      if (path.points.length < 2) return;
      ctx.beginPath();
      ctx.globalAlpha = path.opacity;
      ctx.strokeStyle = path.tool === "eraser" ? "#1a1a2e" : path.color;
      ctx.lineWidth = path.tool === "eraser" ? path.size * 3 : path.size;
      ctx.lineCap = "round";
      ctx.lineJoin = "round";
      ctx.moveTo(path.points[0].x, path.points[0].y);
      path.points.slice(1).forEach(pt => ctx.lineTo(pt.x, pt.y));
      ctx.stroke();
      ctx.globalAlpha = 1;
    });
  }, []);

  useEffect(() => { redraw(paths); }, [paths, redraw]);

  const startDraw = (e: React.MouseEvent | React.TouchEvent) => {
    e.preventDefault();
    const pos = getPos(e);
    const np: DrawPath = {
      id: Date.now().toString(),
      tool: activeTool,
      color: activeColor,
      size: penSize,
      points: [pos],
      opacity: activeTool === "highlighter" ? 0.35 : 1,
    };
    setCurrentPath(np);
    setIsDrawing(true);
  };

  const draw = (e: React.MouseEvent | React.TouchEvent) => {
    e.preventDefault();
    if (!isDrawing || !currentPath) return;
    const pos = getPos(e);
    const updated = { ...currentPath, points: [...currentPath.points, pos] };
    setCurrentPath(updated);
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d")!;
    ctx.beginPath();
    ctx.globalAlpha = updated.opacity;
    ctx.strokeStyle = updated.tool === "eraser" ? "#1a1a2e" : updated.color;
    ctx.lineWidth = updated.tool === "eraser" ? updated.size * 3 : updated.size;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
    const pts = updated.points;
    ctx.moveTo(pts[pts.length - 2].x, pts[pts.length - 2].y);
    ctx.lineTo(pts[pts.length - 1].x, pts[pts.length - 1].y);
    ctx.stroke();
    ctx.globalAlpha = 1;
  };

  const endDraw = () => {
    if (!isDrawing || !currentPath) return;
    const newPaths = [...paths, currentPath];
    setPaths(newPaths);
    const newHistory = history.slice(0, historyIdx + 1);
    newHistory.push(newPaths);
    setHistory(newHistory);
    setHistoryIdx(newHistory.length - 1);
    setCurrentPath(null);
    setIsDrawing(false);
  };

  const undo = () => {
    if (historyIdx <= 0) return;
    const ni = historyIdx - 1;
    setHistoryIdx(ni);
    setPaths(history[ni]);
    redraw(history[ni]);
  };

  const redo = () => {
    if (historyIdx >= history.length - 1) return;
    const ni = historyIdx + 1;
    setHistoryIdx(ni);
    setPaths(history[ni]);
    redraw(history[ni]);
  };

  const clear = () => {
    setPaths([]);
    const h = [...history.slice(0, historyIdx + 1), []];
    setHistory(h);
    setHistoryIdx(h.length - 1);
    const canvas = canvasRef.current;
    if (canvas) canvas.getContext("2d")!.clearRect(0, 0, canvas.width, canvas.height);
  };

  return (
    <div className="flex flex-col h-full">
      {/* Whiteboard topbar */}
      <div className="flex items-center justify-between px-4 py-2 border-b border-white/5 bg-[#0D0D14]/80">
        <div className="flex items-center gap-2">
          <button onClick={onBack} className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg hover:bg-white/10 text-white/60 hover:text-white text-sm transition-colors">
            ← Back
          </button>
          <div className="w-px h-4 bg-white/10" />
          <span className="text-sm font-semibold text-white/80">Whiteboard</span>
        </div>
        <div className="flex items-center gap-2">
          <button onClick={undo} disabled={historyIdx <= 0} className="px-2.5 py-1.5 rounded-lg text-xs text-white/60 hover:text-white hover:bg-white/10 disabled:opacity-30 transition-colors">↩ Undo</button>
          <button onClick={redo} disabled={historyIdx >= history.length - 1} className="px-2.5 py-1.5 rounded-lg text-xs text-white/60 hover:text-white hover:bg-white/10 disabled:opacity-30 transition-colors">↪ Redo</button>
          <button onClick={clear} className="px-2.5 py-1.5 rounded-lg text-xs text-red-400/80 hover:text-red-400 hover:bg-red-500/10 transition-colors">🗑 Clear</button>
        </div>
      </div>
      {/* Canvas */}
      <div className="flex-1 relative overflow-hidden bg-[#1a1a2e]">
        <canvas
          ref={canvasRef}
          width={1400}
          height={900}
          className="absolute inset-0 w-full h-full touch-none"
          style={{ cursor: activeTool === "eraser" ? "cell" : "crosshair" }}
          onMouseDown={startDraw}
          onMouseMove={draw}
          onMouseUp={endDraw}
          onMouseLeave={endDraw}
          onTouchStart={startDraw}
          onTouchMove={draw}
          onTouchEnd={endDraw}
        />
        {/* Grid lines */}
        <div className="absolute inset-0 pointer-events-none opacity-10"
          style={{ backgroundImage: "linear-gradient(#4a4a6a 1px, transparent 1px), linear-gradient(90deg, #4a4a6a 1px, transparent 1px)", backgroundSize: "40px 40px" }} />
      </div>
    </div>
  );
}

// ─── Main Meeting Component ───────────────────────────────────────────────────
export default function MeetingRoom() {
  // Core state
  const [viewMode, setViewMode] = useState<ViewMode>("gallery");
  const [isMuted, setIsMuted] = useState(false);
  const [isCameraOff, setIsCameraOff] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [isHandRaised, setIsHandRaised] = useState(false);
  const [isScreenSharing, setIsScreenSharing] = useState(false);
  const [participants, setParticipants] = useState<Participant[]>(INITIAL_PARTICIPANTS);
  const [messages, setMessages] = useState<ChatMessage[]>(INITIAL_MESSAGES);
  const [chatInput, setChatInput] = useState("");
  const [activeTab, setActiveTab] = useState<Tab>("participants");
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [elapsed, setElapsed] = useState(0);
  const [showEndModal, setShowEndModal] = useState(false);
  const [showInviteModal, setShowInviteModal] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [reactions, setReactions] = useState<{ id: string; emoji: string; x: number; y: number }[]>([]);

  // Whiteboard state
  const [activeTool, setActiveTool] = useState<Tool>("pen");
  const [activeColor, setActiveColor] = useState("#007AFF");
  const [penSize, setPenSize] = useState(3);

  // Timer
  useEffect(() => {
    const t = setInterval(() => setElapsed(e => e + 1), 1000);
    return () => clearInterval(t);
  }, []);

  const formatTime = (s: number) => {
    const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), sec = s % 60;
    return h > 0 ? `${h}:${String(m).padStart(2, "0")}:${String(sec).padStart(2, "0")}` : `${m}:${String(sec).padStart(2, "0")}`;
  };

  const sendMessage = () => {
    if (!chatInput.trim()) return;
    setMessages(prev => [...prev, {
      id: Date.now().toString(), sender: "You", text: chatInput, time: new Date().toLocaleTimeString("en", { hour: "2-digit", minute: "2-digit" }), isMe: true,
    }]);
    setChatInput("");
  };

  const sendReaction = (emoji: string) => {
    const id = Date.now().toString();
    setReactions(prev => [...prev, { id, emoji, x: Math.random() * 60 + 20, y: Math.random() * 40 + 30 }]);
    setTimeout(() => setReactions(prev => prev.filter(r => r.id !== id)), 2500);
  };

  const messagesEndRef = useRef<HTMLDivElement>(null);
  useEffect(() => { messagesEndRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);

  const tools: { id: Tool; icon: string; label: string }[] = [
    { id: "select", icon: "↖", label: "Select" },
    { id: "pen", icon: "✏️", label: "Pen" },
    { id: "highlighter", icon: "🖊", label: "Highlight" },
    { id: "eraser", icon: "⌫", label: "Eraser" },
    { id: "shape", icon: "⬜", label: "Shape" },
    { id: "text", icon: "T", label: "Text" },
  ];

  return (
    <div className="flex flex-col h-screen bg-[#0D0D14] text-white overflow-hidden font-sans select-none">
      {/* ── Top Bar ── */}
      <header className="flex items-center justify-between px-4 py-2.5 border-b border-white/5 bg-[#0D0D14]/95 backdrop-blur-md z-30 flex-shrink-0">
        {/* Left */}
        <div className="flex items-center gap-4 min-w-0">
          <div className="flex items-center gap-2.5">
            <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-[#007AFF] to-[#5856D6] flex items-center justify-center text-xs font-bold">M</div>
            <div>
              <div className="text-sm font-semibold text-white leading-none">Q3 Strategy Sync</div>
              <div className="text-[11px] text-white/40 leading-none mt-0.5 hidden sm:block">Team Standup • Daily</div>
            </div>
          </div>
          {/* Timer + Recording */}
          <div className="flex items-center gap-2">
            <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-white/5 border border-white/5">
              <div className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              <span className="text-xs font-mono text-white/70">{formatTime(elapsed)}</span>
            </div>
            {isRecording && (
              <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-red-500/15 border border-red-500/30 animate-pulse">
                <div className="w-1.5 h-1.5 rounded-full bg-red-500" />
                <span className="text-xs font-semibold text-red-400">REC</span>
              </div>
            )}
          </div>
        </div>
        {/* Center — view mode */}
        <div className="hidden md:flex items-center gap-1 p-1 rounded-xl bg-white/5 border border-white/5">
          {(["gallery", "spotlight", "whiteboard"] as ViewMode[]).map(mode => (
            <button key={mode} onClick={() => setViewMode(mode)}
              className={`px-3 py-1 rounded-lg text-xs font-medium capitalize transition-all ${viewMode === mode ? "bg-white/10 text-white" : "text-white/40 hover:text-white/70"}`}>
              {mode === "gallery" ? "⊞ Gallery" : mode === "spotlight" ? "⊡ Spotlight" : "✏ Board"}
            </button>
          ))}
        </div>
        {/* Right */}
        <div className="flex items-center gap-2">
          <span className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-lg bg-white/5 text-xs text-white/50">
            <span>👥</span> {participants.length}
          </span>
          <button onClick={() => setShowInviteModal(true)} className="hidden sm:flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#007AFF]/20 hover:bg-[#007AFF]/30 border border-[#007AFF]/30 text-[#007AFF] text-xs font-semibold transition-colors">
            + Invite
          </button>
          <button onClick={() => setSidebarOpen(s => !s)} className="p-2 rounded-lg hover:bg-white/10 text-white/50 hover:text-white transition-colors text-sm">
            {sidebarOpen ? "⟩" : "⟨"}
          </button>
          <button onClick={() => setShowEndModal(true)} className="px-3 py-1.5 rounded-lg bg-red-500/20 hover:bg-red-500/30 border border-red-500/30 text-red-400 text-xs font-bold transition-colors">
            End
          </button>
        </div>
      </header>

      {/* ── Main Content ── */}
      <div className="flex flex-1 overflow-hidden">
        {/* ── Left: Whiteboard Toolbar (only in whiteboard mode) ── */}
        {viewMode === "whiteboard" && (
          <aside className="flex flex-col items-center gap-3 px-2 py-4 border-r border-white/5 bg-[#0D0D14]/80 z-20 w-14 md:w-16">
            <div className="flex flex-col gap-1">
              {tools.map(t => (
                <button key={t.id} title={t.label} onClick={() => setActiveTool(t.id)}
                  className={`w-9 h-9 md:w-10 md:h-10 rounded-xl flex items-center justify-center text-sm transition-all ${activeTool === t.id ? "bg-[#007AFF] text-white shadow-lg shadow-blue-500/30" : "hover:bg-white/10 text-white/50 hover:text-white"}`}>
                  {t.icon}
                </button>
              ))}
            </div>
            <div className="w-8 h-px bg-white/10" />
            {/* Colors */}
            <div className="flex flex-col gap-1.5">
              {PEN_COLORS.slice(0, 8).map(c => (
                <button key={c} onClick={() => setActiveColor(c)}
                  className={`w-5 h-5 rounded-full transition-all ${activeColor === c ? "ring-2 ring-white ring-offset-1 ring-offset-[#0D0D14] scale-110" : "opacity-70 hover:opacity-100"}`}
                  style={{ background: c }} />
              ))}
            </div>
            <div className="w-8 h-px bg-white/10" />
            {/* Pen size */}
            <div className="flex flex-col items-center gap-1">
              {[2, 4, 7].map(s => (
                <button key={s} onClick={() => setPenSize(s)}
                  className={`flex items-center justify-center w-9 h-6 rounded-lg transition-colors ${penSize === s ? "bg-white/15" : "hover:bg-white/5"}`}>
                  <div className="rounded-full bg-white/80" style={{ width: s * 2, height: s * 2 }} />
                </button>
              ))}
            </div>
          </aside>
        )}

        {/* ── Center: Video / Whiteboard ── */}
        <main className="flex-1 flex flex-col min-w-0 overflow-hidden">
          {viewMode === "whiteboard" ? (
            <Whiteboard activeTool={activeTool} activeColor={activeColor} penSize={penSize} onBack={() => setViewMode("gallery")} />
          ) : viewMode === "spotlight" ? (
            <div className="flex-1 flex flex-col p-3 gap-3 overflow-hidden">
              <div className="flex-1 min-h-0">
                <VideoTile p={participants.find(p => p.isActive) || participants[0]} large />
              </div>
              <div className="flex gap-2 overflow-x-auto pb-1 flex-shrink-0">
                {participants.filter((_, i) => i !== 0).map(p => (
                  <div key={p.id} className="w-28 flex-shrink-0" onClick={() => setParticipants(prev => prev.map(pp => ({ ...pp, isActive: pp.id === p.id })))}>
                    <VideoTile p={p} />
                  </div>
                ))}
              </div>
            </div>
          ) : (
            // Gallery view
            <div className="flex-1 p-3 overflow-auto">
              <div className="grid gap-2 h-full"
                style={{ gridTemplateColumns: `repeat(${Math.min(participants.length <= 2 ? 2 : participants.length <= 4 ? 2 : 3, 3)}, 1fr)` }}>
                {participants.map(p => <VideoTile key={p.id} p={p} />)}
              </div>
            </div>
          )}

          {/* ── Bottom Controls ── */}
          <div className="flex-shrink-0 flex items-center justify-center gap-2 md:gap-3 px-4 py-3 border-t border-white/5 bg-[#0D0D14]/95 backdrop-blur-md flex-wrap">
            {/* Mic */}
            <button onClick={() => setIsMuted(m => !m)}
              className={`flex flex-col items-center gap-1 p-2.5 md:p-3 rounded-2xl transition-all ${isMuted ? "bg-red-500/20 border border-red-500/40 text-red-400" : "bg-white/5 hover:bg-white/10 text-white/70 hover:text-white border border-transparent"}`}>
              <span className="text-lg">{isMuted ? "🔇" : "🎤"}</span>
              <span className="text-[10px] hidden sm:block">{isMuted ? "Unmute" : "Mute"}</span>
            </button>
            {/* Camera */}
            <button onClick={() => setIsCameraOff(c => !c)}
              className={`flex flex-col items-center gap-1 p-2.5 md:p-3 rounded-2xl transition-all ${isCameraOff ? "bg-red-500/20 border border-red-500/40 text-red-400" : "bg-white/5 hover:bg-white/10 text-white/70 hover:text-white border border-transparent"}`}>
              <span className="text-lg">{isCameraOff ? "📷" : "📹"}</span>
              <span className="text-[10px] hidden sm:block">{isCameraOff ? "Start Cam" : "Stop Cam"}</span>
            </button>
            {/* Screen Share */}
            <button onClick={() => setIsScreenSharing(s => !s)}
              className={`flex flex-col items-center gap-1 p-2.5 md:p-3 rounded-2xl transition-all ${isScreenSharing ? "bg-[#007AFF]/20 border border-[#007AFF]/40 text-[#007AFF]" : "bg-white/5 hover:bg-white/10 text-white/70 hover:text-white border border-transparent"}`}>
              <span className="text-lg">🖥️</span>
              <span className="text-[10px] hidden sm:block">Share</span>
            </button>
            {/* Whiteboard */}
            <button onClick={() => setViewMode(v => v === "whiteboard" ? "gallery" : "whiteboard")}
              className={`flex flex-col items-center gap-1 p-2.5 md:p-3 rounded-2xl transition-all ${viewMode === "whiteboard" ? "bg-[#5856D6]/20 border border-[#5856D6]/40 text-[#5856D6]" : "bg-white/5 hover:bg-white/10 text-white/70 hover:text-white border border-transparent"}`}>
              <span className="text-lg">✏️</span>
              <span className="text-[10px] hidden sm:block">Board</span>
            </button>
            {/* Record */}
            <button onClick={() => setIsRecording(r => !r)}
              className={`flex flex-col items-center gap-1 p-2.5 md:p-3 rounded-2xl transition-all ${isRecording ? "bg-red-500/20 border border-red-500/40 text-red-400 animate-pulse" : "bg-white/5 hover:bg-white/10 text-white/70 hover:text-white border border-transparent"}`}>
              <span className="text-lg">⏺️</span>
              <span className="text-[10px] hidden sm:block">{isRecording ? "Stop Rec" : "Record"}</span>
            </button>
            {/* Hand */}
            <button onClick={() => setIsHandRaised(h => !h)}
              className={`flex flex-col items-center gap-1 p-2.5 md:p-3 rounded-2xl transition-all ${isHandRaised ? "bg-[#FF9500]/20 border border-[#FF9500]/40 text-[#FF9500]" : "bg-white/5 hover:bg-white/10 text-white/70 hover:text-white border border-transparent"}`}>
              <span className="text-lg">✋</span>
              <span className="text-[10px] hidden sm:block">Raise</span>
            </button>
            {/* Reactions */}
            <div className="relative group">
              <button className="flex flex-col items-center gap-1 p-2.5 md:p-3 rounded-2xl bg-white/5 hover:bg-white/10 text-white/70 hover:text-white border border-transparent transition-all">
                <span className="text-lg">😊</span>
                <span className="text-[10px] hidden sm:block">React</span>
              </button>
              <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 hidden group-hover:flex gap-1.5 bg-[#1C1C2E] border border-white/10 rounded-2xl px-2 py-2 shadow-2xl">
                {["👍", "❤️", "😂", "🎉", "👏", "🔥"].map(e => (
                  <button key={e} onClick={() => sendReaction(e)} className="text-xl hover:scale-125 transition-transform">{e}</button>
                ))}
              </div>
            </div>
            {/* Settings */}
            <button onClick={() => setShowSettings(true)} className="flex flex-col items-center gap-1 p-2.5 md:p-3 rounded-2xl bg-white/5 hover:bg-white/10 text-white/70 hover:text-white border border-transparent transition-all">
              <span className="text-lg">⚙️</span>
              <span className="text-[10px] hidden sm:block">Settings</span>
            </button>
          </div>
        </main>

        {/* ── Right Sidebar ── */}
        {sidebarOpen && (
          <aside className="w-72 md:w-80 flex flex-col border-l border-white/5 bg-[#0D0D14]/80 flex-shrink-0">
            {/* Tabs */}
            <div className="flex border-b border-white/5 flex-shrink-0">
              {(["participants", "chat", "settings"] as Tab[]).map(t => (
                <button key={t} onClick={() => setActiveTab(t)}
                  className={`flex-1 py-2.5 text-xs font-semibold capitalize transition-colors relative ${activeTab === t ? "text-white" : "text-white/40 hover:text-white/70"}`}>
                  {t === "participants" ? `👥 People (${participants.length})` : t === "chat" ? `💬 Chat` : "⚙ More"}
                  {activeTab === t && <div className="absolute bottom-0 left-1/4 right-1/4 h-0.5 bg-[#007AFF] rounded-full" />}
                </button>
              ))}
            </div>

            {/* Participants */}
            {activeTab === "participants" && (
              <div className="flex-1 overflow-y-auto py-2">
                {/* Host section */}
                {["host", "co-host", "participant"].map(role => {
                  const group = participants.filter(p => p.role === role);
                  if (!group.length) return null;
                  return (
                    <div key={role} className="mb-2">
                      <div className="px-4 py-1.5 text-[10px] uppercase tracking-widest text-white/30 font-bold">{role}s ({group.length})</div>
                      {group.map(p => <ParticipantCard key={p.id} p={p} isHost />)}
                    </div>
                  );
                })}
                <div className="px-4 pt-3 pb-2">
                  <button onClick={() => setShowInviteModal(true)}
                    className="w-full py-2 rounded-xl border border-dashed border-white/15 text-white/40 hover:text-white/70 hover:border-white/30 text-xs transition-colors">
                    + Invite participants
                  </button>
                </div>
              </div>
            )}

            {/* Chat */}
            {activeTab === "chat" && (
              <>
                <div className="flex-1 overflow-y-auto px-3 py-3 space-y-3">
                  {messages.map(msg => (
                    <div key={msg.id} className={`flex gap-2 ${msg.isMe ? "flex-row-reverse" : ""}`}>
                      {!msg.isMe && (
                        <div className="w-7 h-7 rounded-full bg-[#007AFF]/20 border border-[#007AFF]/30 flex items-center justify-center text-[10px] font-bold text-[#007AFF] flex-shrink-0 mt-0.5">
                          {msg.sender.split(" ").map(s => s[0]).join("").slice(0, 2)}
                        </div>
                      )}
                      <div className={`max-w-[75%] ${msg.isMe ? "items-end" : "items-start"} flex flex-col gap-0.5`}>
                        {!msg.isMe && <span className="text-[10px] text-white/40 pl-0.5">{msg.sender}</span>}
                        <div className={`px-3 py-2 rounded-2xl text-sm leading-snug ${msg.isMe ? "bg-[#007AFF] text-white rounded-tr-sm" : "bg-white/8 text-white/90 rounded-tl-sm"}`}>
                          {msg.text}
                        </div>
                        <span className="text-[9px] text-white/25 px-0.5">{msg.time}</span>
                      </div>
                    </div>
                  ))}
                  <div ref={messagesEndRef} />
                </div>
                <div className="p-3 border-t border-white/5 flex-shrink-0">
                  <div className="flex gap-2">
                    <input value={chatInput} onChange={e => setChatInput(e.target.value)}
                      onKeyDown={e => e.key === "Enter" && sendMessage()}
                      placeholder="Type a message…"
                      className="flex-1 bg-white/5 border border-white/10 rounded-xl px-3 py-2 text-sm text-white placeholder-white/30 focus:outline-none focus:border-[#007AFF]/50 focus:bg-white/8 transition-all" />
                    <button onClick={sendMessage} className="px-3 py-2 rounded-xl bg-[#007AFF] hover:bg-[#0066DD] text-white text-sm transition-colors">↑</button>
                  </div>
                </div>
              </>
            )}

            {/* More / settings tab */}
            {activeTab === "settings" && (
              <div className="flex-1 overflow-y-auto px-3 py-3 space-y-3">
                {[
                  { label: "Lock meeting", icon: "🔒", desc: "Prevent new participants" },
                  { label: "Mute all", icon: "🔇", desc: "Mute all participants" },
                  { label: "Disable video all", icon: "📷", desc: "Turn off all cameras" },
                  { label: "Allow reactions", icon: "😊", desc: "Enable emoji reactions" },
                  { label: "Enable waiting room", icon: "🚪", desc: "Admit participants manually" },
                  { label: "Closed captions", icon: "💬", desc: "Show live captions" },
                  { label: "Virtual background", icon: "🌅", desc: "Change your background" },
                  { label: "Noise suppression", icon: "🔈", desc: "Reduce background noise" },
                  { label: "Breakout rooms", icon: "🏠", desc: "Split into smaller groups" },
                  { label: "Live stream", icon: "📡", desc: "Stream to YouTube / Twitch" },
                ].map(item => (
                  <div key={item.label} className="flex items-center justify-between p-3 rounded-xl hover:bg-white/5 border border-transparent hover:border-white/5 transition-all cursor-pointer group">
                    <div className="flex items-center gap-3">
                      <span className="text-lg">{item.icon}</span>
                      <div>
                        <div className="text-sm text-white/80 font-medium group-hover:text-white transition-colors">{item.label}</div>
                        <div className="text-xs text-white/35">{item.desc}</div>
                      </div>
                    </div>
                    <div className="w-10 h-5 rounded-full bg-white/10 relative flex-shrink-0">
                      <div className="absolute left-0.5 top-0.5 w-4 h-4 rounded-full bg-white/30 transition-all" />
                    </div>
                  </div>
                ))}
              </div>
            )}
          </aside>
        )}
      </div>

      {/* ── Floating Reactions ── */}
      {reactions.map(r => (
        <div key={r.id} className="fixed text-3xl pointer-events-none z-50 animate-bounce"
          style={{ left: `${r.x}%`, top: `${r.y}%`, animation: "floatUp 2.5s ease-out forwards" }}>
          {r.emoji}
        </div>
      ))}

      {/* ── End Meeting Modal ── */}
      {showEndModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#1C1C2E] border border-white/10 rounded-2xl p-6 w-full max-w-sm shadow-2xl">
            <h3 className="text-lg font-bold text-white mb-1">End Meeting?</h3>
            <p className="text-sm text-white/50 mb-6">This will end the meeting for everyone.</p>
            <div className="flex gap-2">
              <button onClick={() => setShowEndModal(false)} className="flex-1 py-2.5 rounded-xl bg-white/5 hover:bg-white/10 text-white/70 text-sm font-semibold transition-colors">Cancel</button>
              <button className="flex-1 py-2.5 rounded-xl bg-red-500 hover:bg-red-600 text-white text-sm font-bold transition-colors">End for All</button>
            </div>
            <button className="w-full mt-2 py-2.5 rounded-xl border border-red-500/30 hover:bg-red-500/10 text-red-400 text-sm font-medium transition-colors">Leave (keep meeting)</button>
          </div>
        </div>
      )}

      {/* ── Invite Modal ── */}
      {showInviteModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#1C1C2E] border border-white/10 rounded-2xl p-6 w-full max-w-sm shadow-2xl">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-white">Invite People</h3>
              <button onClick={() => setShowInviteModal(false)} className="text-white/40 hover:text-white text-xl transition-colors">✕</button>
            </div>
            <div className="bg-white/5 border border-white/10 rounded-xl px-3 py-3 flex items-center justify-between mb-3">
              <span className="text-sm text-white/60 font-mono">meet.app/q3-sync-x7k2</span>
              <button className="text-xs text-[#007AFF] font-semibold hover:text-[#5AC8FA] transition-colors">Copy</button>
            </div>
            <div className="text-center text-white/30 text-xs mb-3">— or share via —</div>
            <div className="grid grid-cols-3 gap-2">
              {["Email", "Slack", "Teams"].map(app => (
                <button key={app} className="py-2 rounded-xl bg-white/5 hover:bg-white/10 text-white/60 text-xs font-medium transition-colors">{app}</button>
              ))}
            </div>
          </div>
        </div>
      )}

      <style>{`
        @keyframes floatUp {
          0% { opacity: 1; transform: translateY(0) scale(1); }
          100% { opacity: 0; transform: translateY(-80px) scale(1.4); }
        }
      `}</style>
    </div>
  );
}
