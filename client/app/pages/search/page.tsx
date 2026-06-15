"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getUser } from "../../services/authService";
import { API_BASE_URL } from "@/app/config/api";

type Module = {
    module_id: number;
    name: string;
    description?: string;
    skills: string[];
    cover_image?: string;
    cover_image_name?: string;
};

const HomePage = () => {
    const [user, setUser] = useState<{ id: number; email: string } | null>(null);
    const [modules, setModules] = useState<Module[]>([]);
    const [publicModules, setPublicModules] = useState<Module[]>([]);
    const [loading, setLoading] = useState(false);
    const [showAllPublic, setShowAllPublic] = useState(false);

    const PUBLIC_LIMIT = 8;

    useEffect(() => {
        const currentUser = getUser();
        setUser(currentUser);
    }, []);

    useEffect(() => {
        if (!user) return;
        const fetchModules = async () => {
            setLoading(true);
            try {
                const res = await fetch(`${API_BASE_URL}/modules/user/${user.id}`);
                if (!res.ok) throw new Error("Failed to fetch modules");
                const data = await res.json();
                setModules(data);
            } catch (error) {
                console.error("Your modules fetch error:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchModules();
    }, [user]);

    useEffect(() => {
        const fetchPublicModules = async () => {
            try {
                const res = await fetch(`${API_BASE_URL}/modules/public`);
                if (!res.ok) throw new Error("Failed to fetch public modules");
                const data = await res.json();
                setPublicModules(data);
            } catch (error) {
                console.error("Public modules fetch error:", error);
            }
        };
        fetchPublicModules();
    }, []);

    const displayedPublicModules = showAllPublic
        ? publicModules
        : publicModules.slice(0, PUBLIC_LIMIT);

    return (
        <div className="bg-white text-slate-900 min-h-screen font-sans antialiased">

            {/* ── NAV STRIP ─────────────────────────────────────────────── */}
            <header className="sticky top-0 z-50 bg-white/90 backdrop-blur border-b border-slate-100">
                <div className="max-w-7xl mx-auto px-6 h-14 flex items-center justify-between">
                    <span className="font-extrabold text-lg tracking-tight text-slate-900">
                        Edu<span className="text-indigo-600">Mate</span>
                    </span>
                    <nav className="hidden md:flex items-center gap-6 text-sm font-medium text-slate-500">
                        <Link href="#explore-section" className="hover:text-slate-900 transition-colors">Explore</Link>
                        <Link href="/pages/create_chanel" className="hover:text-slate-900 transition-colors">Create</Link>
                    </nav>
                    <Link
                        href="/pages/create_chanel"
                        className="text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 px-4 py-2 rounded-lg transition-colors"
                    >
                        Get Started
                    </Link>
                </div>
            </header>

            {/* ── HERO ──────────────────────────────────────────────────── */}
            <section className="relative overflow-hidden bg-white">
                {/* Large indigo geometric accent — the signature element */}
                <div
                    aria-hidden
                    className="absolute right-0 top-0 w-[55%] h-full bg-indigo-50 [clip-path:polygon(12%_0%,100%_0%,100%_100%,0%_100%)] pointer-events-none"
                />
                {/* Dot-grid texture on the indigo panel */}
                <div
                    aria-hidden
                    className="absolute right-0 top-0 w-[55%] h-full opacity-30 pointer-events-none"
                    style={{
                        backgroundImage:
                            "radial-gradient(circle, #818cf8 1px, transparent 1px)",
                        backgroundSize: "28px 28px",
                        clipPath: "polygon(12% 0%, 100% 0%, 100% 100%, 0% 100%)",
                    }}
                />

                <div className="relative max-w-7xl mx-auto px-6 py-24 lg:py-36 grid lg:grid-cols-2 gap-16 items-center">
                    {/* LEFT — copy */}
                    <div>
                        <span className="inline-block text-[11px] font-bold tracking-[0.18em] uppercase text-indigo-600 mb-5">
                            Learning Management System
                        </span>
                        <h1 className="text-5xl lg:text-6xl font-extrabold leading-[1.05] tracking-tight text-slate-900 mb-6">
                            Smart paths for{" "}
                            <em className="not-italic text-indigo-600">every</em>{" "}
                            learner.
                        </h1>
                        <p className="text-base text-slate-500 leading-relaxed max-w-md mb-10">
                            EduMate unifies digital assessments, structured curricula, and AI-powered insights so students and educators move forward together.
                        </p>
                        <div className="flex flex-wrap gap-3">
                            <Link
                                href="#explore-section"
                                className="inline-flex items-center gap-2 px-6 py-3 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold rounded-xl shadow-md shadow-indigo-200 transition-all"
                            >
                                Browse Modules
                                <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                                </svg>
                            </Link>
                            <Link
                                href="/pages/create_chanel"
                                className="inline-flex items-center gap-2 px-6 py-3 bg-white hover:bg-slate-50 text-slate-700 text-sm font-semibold rounded-xl border border-slate-200 transition-all"
                            >
                                Create a Hub
                            </Link>
                        </div>
                    </div>

                    {/* RIGHT — floating stats card */}
                    <div className="relative flex justify-center lg:justify-end">
                        <div className="relative bg-white rounded-3xl shadow-2xl shadow-slate-200 p-8 w-full max-w-sm border border-slate-100">
                            {/* accent corner */}
                            <div className="absolute -top-4 -right-4 w-16 h-16 bg-indigo-600 rounded-2xl rotate-12" />

                            <p className="text-[11px] font-bold tracking-widest uppercase text-slate-400 mb-6">
                                Platform at a glance
                            </p>

                            <div className="space-y-5">
                                {[
                                    { label: "AI-Driven Study Paths", icon: "✦", color: "text-indigo-600" },
                                    { label: "Centralized Syllabi Portals", icon: "◈", color: "text-violet-500" },
                                    { label: "Interactive Assessments", icon: "◉", color: "text-sky-500" },
                                    { label: "Real-Time Progress Tracking", icon: "▲", color: "text-emerald-500" },
                                ].map((item) => (
                                    <div key={item.label} className="flex items-center gap-4">
                                        <span className={`text-lg font-bold ${item.color} w-6 flex-shrink-0`}>
                                            {item.icon}
                                        </span>
                                        <span className="text-sm font-medium text-slate-700">{item.label}</span>
                                    </div>
                                ))}
                            </div>

                            <div className="mt-8 pt-6 border-t border-slate-100 flex items-center justify-between">
                                <span className="text-xs text-slate-400">Trusted by educators worldwide</span>
                                <div className="flex -space-x-2">
                                    {["bg-indigo-400", "bg-violet-400", "bg-sky-400", "bg-emerald-400"].map((c, i) => (
                                        <div key={i} className={`w-7 h-7 rounded-full border-2 border-white ${c}`} />
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* ── ANNOUNCEMENT STRIP ───────────────────────────────────── */}
            <div className="bg-indigo-600 py-2.5 text-center">
                <Link href="#" className="inline-flex items-center gap-2 text-sm text-indigo-100 hover:text-white transition-colors">
                    <span className="text-[10px] font-bold tracking-wider uppercase bg-white text-indigo-600 px-2 py-0.5 rounded-full">
                        New
                    </span>
                    EduMate v2.0 — AI-powered analytics paths are live
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                    </svg>
                </Link>
            </div>

            {/* ── USER WORKSPACE ───────────────────────────────────────── */}
            {user && (
                <section className="max-w-7xl mx-auto px-6 pt-20 pb-6">
                    <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-10">
                        <div>
                            <span className="text-[11px] font-bold tracking-[0.18em] uppercase text-indigo-500">
                                Your Account
                            </span>
                            <h2 className="text-2xl font-extrabold text-slate-900 mt-1 tracking-tight">
                                Learning Workspace
                            </h2>
                            <p className="text-sm text-slate-400 mt-1">
                                Modules you own or are actively enrolled in.
                            </p>
                        </div>
                        <Link
                            href="/pages/create_chanel"
                            className="mt-4 sm:mt-0 inline-flex items-center gap-1.5 text-xs font-bold text-indigo-600 hover:text-indigo-800 border border-indigo-200 bg-indigo-50 hover:bg-indigo-100 px-4 py-2 rounded-lg transition-all self-start"
                        >
                            <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M12 4v16m8-8H4" />
                            </svg>
                            New Module
                        </Link>
                    </div>

                    {loading ? (
                        <div className="py-16 text-center">
                            <div className="inline-flex gap-1.5">
                                {[0, 0.15, 0.3].map((d, i) => (
                                    <div
                                        key={i}
                                        className="w-2 h-2 bg-indigo-400 rounded-full animate-bounce"
                                        style={{ animationDelay: `${d}s` }}
                                    />
                                ))}
                            </div>
                            <p className="text-sm text-slate-400 mt-3">Loading your workspace…</p>
                        </div>
                    ) : modules.length === 0 ? (
                        <div className="border-2 border-dashed border-slate-200 rounded-2xl p-14 text-center bg-slate-50">
                            <div className="w-12 h-12 bg-indigo-100 rounded-2xl flex items-center justify-center mx-auto mb-4">
                                <svg className="w-6 h-6 text-indigo-600" fill="none" stroke="currentColor" strokeWidth={1.5} viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                                </svg>
                            </div>
                            <p className="text-sm font-semibold text-slate-600">No modules yet</p>
                            <p className="text-xs text-slate-400 mt-1">Create one or enroll in a public path below.</p>
                        </div>
                    ) : (
                        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                            {modules.map((module, idx) => (
                                <div
                                    key={module.module_id}
                                    className="group relative bg-white border border-slate-200 rounded-2xl overflow-hidden hover:shadow-xl hover:shadow-slate-200/70 hover:-translate-y-1 transition-all duration-300 flex flex-col"
                                >
                                    {/* Colored top accent bar per card */}
                                    <div
                                        className="absolute top-0 left-0 right-0 h-1 rounded-t-2xl"
                                        style={{ background: ["#6366f1", "#8b5cf6", "#3b82f6", "#10b981"][idx % 4] }}
                                    />

                                    <div className="overflow-hidden relative h-36 w-full bg-slate-100 mt-1">
                                        <img
                                            className="h-full w-full object-cover group-hover:scale-105 transition-transform duration-500"
                                            src={
                                                module.cover_image
                                                    ? `data:image/png;base64,${module.cover_image}`
                                                    : "/images/Tree life-rafiki.png"
                                            }
                                            alt={module.name}
                                        />
                                        <div className="absolute inset-0 bg-gradient-to-t from-white/20 to-transparent" />
                                    </div>

                                    <div className="p-5 flex flex-col flex-grow">
                                        <span className="text-[10px] font-bold tracking-widest uppercase text-indigo-500 mb-1">
                                            Workspace
                                        </span>
                                        <h3 className="text-sm font-bold text-slate-900 line-clamp-1 group-hover:text-indigo-600 transition-colors">
                                            {module.name}
                                        </h3>
                                        <p className="text-xs text-slate-400 mt-2 line-clamp-2 leading-relaxed flex-grow">
                                            {module.description || "No description available for this module."}
                                        </p>
                                        <div className="pt-4 mt-4 border-t border-slate-100">
                                            <Link
                                                href={`/enrolle/${module.module_id}`}
                                                className="inline-flex items-center gap-1.5 text-xs font-semibold text-indigo-600 hover:text-indigo-800 transition-colors"
                                            >
                                                Enter Workspace
                                                <svg className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24">
                                                    <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                                                </svg>
                                            </Link>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </section>
            )}

            {/* ── DIVIDER ──────────────────────────────────────────────── */}
            <div className="max-w-7xl mx-auto px-6 py-8">
                <div className="h-px bg-gradient-to-r from-transparent via-slate-200 to-transparent" />
            </div>

            {/* ── PUBLIC MODULES ───────────────────────────────────────── */}
            <section id="explore-section" className="max-w-7xl mx-auto px-6 pb-24">
                <div className="flex flex-col sm:flex-row sm:items-end justify-between mb-10">
                    <div>
                        <span className="text-[11px] font-bold tracking-[0.18em] uppercase text-emerald-600">
                            Open Access
                        </span>
                        <h2 className="text-2xl font-extrabold text-slate-900 mt-1 tracking-tight">
                            Global Knowledge Exchange
                        </h2>
                        <p className="text-sm text-slate-400 mt-1">
                            Open-access curricula published by certified EduMate creators.
                        </p>
                    </div>
                    <span className="text-xs text-slate-400 mt-2 sm:mt-0 font-medium">
                        {displayedPublicModules.length} / {publicModules.length} modules
                    </span>
                </div>

                {publicModules.length === 0 ? (
                    <div className="py-16 text-center text-slate-400 text-sm">
                        No public modules available yet. Check back soon.
                    </div>
                ) : (
                    <>
                        <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
                            {displayedPublicModules.map((module, idx) => (
                                <div
                                    key={module.module_id}
                                    className="group bg-white border border-slate-200 rounded-2xl overflow-hidden hover:shadow-lg hover:shadow-slate-200/60 hover:-translate-y-0.5 transition-all duration-300 flex flex-col"
                                >
                                    <div className="overflow-hidden relative h-36 w-full bg-slate-100">
                                        <img
                                            className="h-full w-full object-cover group-hover:scale-105 transition-transform duration-500"
                                            src={
                                                module.cover_image
                                                    ? `data:image/png;base64,${module.cover_image}`
                                                    : "/images/Tree life-rafiki.png"
                                            }
                                            alt={module.name}
                                        />
                                        {/* Emerald badge */}
                                        <div className="absolute top-3 left-3 bg-white text-emerald-600 border border-emerald-200 text-[10px] uppercase font-bold px-2 py-0.5 rounded-full shadow-sm">
                                            Public
                                        </div>
                                    </div>

                                    <div className="p-5 flex flex-col flex-grow">
                                        {/* mini progress bar — purely decorative, indicates "completeness" variety */}
                                        <div className="h-0.5 w-full bg-slate-100 rounded-full mb-3 overflow-hidden">
                                            <div
                                                className="h-full bg-emerald-400 rounded-full"
                                                style={{ width: `${25 + (idx % 4) * 18}%` }}
                                            />
                                        </div>

                                        <h3 className="text-sm font-bold text-slate-900 line-clamp-1">
                                            {module.name}
                                        </h3>
                                        <p className="text-xs text-slate-400 mt-2 line-clamp-2 leading-relaxed flex-grow">
                                            {module.description || "No overview documentation structured."}
                                        </p>

                                        <div className="pt-4 mt-4 border-t border-slate-100">
                                            <Link
                                                href={`/enrolle/${module.module_id}`}
                                                className="inline-flex justify-center items-center w-full py-2.5 px-4 text-xs font-semibold text-indigo-600 bg-indigo-50 hover:bg-indigo-100 rounded-xl transition-colors group-hover:shadow-sm"
                                            >
                                                Explore Curriculum
                                                <svg className="w-3.5 h-3.5 ml-1.5 group-hover:translate-x-0.5 transition-transform" fill="none" stroke="currentColor" strokeWidth={2.5} viewBox="0 0 24 24">
                                                    <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                                                </svg>
                                            </Link>
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>

                        {publicModules.length > PUBLIC_LIMIT && (
                            <div className="mt-12 text-center">
                                <button
                                    onClick={() => setShowAllPublic(!showAllPublic)}
                                    className="inline-flex items-center gap-2 px-6 py-3 text-sm font-semibold text-slate-700 bg-white border border-slate-200 hover:border-slate-300 hover:shadow-md rounded-xl transition-all"
                                >
                                    {showAllPublic ? (
                                        <>
                                            Show fewer modules
                                            <svg className="w-4 h-4 rotate-180" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
                                            </svg>
                                        </>
                                    ) : (
                                        <>
                                            View all {publicModules.length - PUBLIC_LIMIT} more paths
                                            <svg className="w-4 h-4" fill="none" stroke="currentColor" strokeWidth={2} viewBox="0 0 24 24">
                                                <path strokeLinecap="round" strokeLinejoin="round" d="M19 9l-7 7-7-7" />
                                            </svg>
                                        </>
                                    )}
                                </button>
                            </div>
                        )}
                    </>
                )}
            </section>

            {/* ── FOOTER ───────────────────────────────────────────────── */}
            <footer className="border-t border-slate-100 bg-slate-50 py-8">
                <div className="max-w-7xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-4">
                    <span className="font-extrabold text-base tracking-tight text-slate-800">
                        Edu<span className="text-indigo-600">Mate</span>
                    </span>
                    <p className="text-xs text-slate-400 text-center">
                        © {new Date().getFullYear()} EduMate Platforms Inc. Adaptive digital learning tools.
                    </p>
                    <div className="flex gap-4 text-xs text-slate-400">
                        <Link href="#" className="hover:text-slate-700 transition-colors">Privacy</Link>
                        <Link href="#" className="hover:text-slate-700 transition-colors">Terms</Link>
                        <Link href="#" className="hover:text-slate-700 transition-colors">Support</Link>
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default HomePage;