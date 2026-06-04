"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { API_BASE_URL } from "@/app/config/api";

interface ChannelData {
    channel_id: number;
    user_id: number;
    channel_name: string;
    description: string | null;
    institute_legal_name: string;
    institute_owner_full_name: string;
    physical_corporate_address: string | null;
    co_hosts_and_faculty_members: string[];
    visibility: "public" | "private";
    official_website_link: string | null;
    facebook_portal_link: string | null;
    cover_image: string | null;
    logo_image: string | null;
}

export default function ChannelDashboardView() {
    const params = useParams();
    const router = useRouter();
    const channelId = params?.id;

    const [channel, setChannel] = useState<ChannelData | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!channelId) return;

        const fetchChannelNode = async () => {
            try {
                setLoading(true);
                // Connecting explicitly to your updated /get/{channel_id} backend framework
                const response = await fetch(`${API_BASE_URL}/channels/${channelId}`);;

                if (!response.ok) {
                    if (response.status === 404) throw new Error("The requested academic hub index does not exist.");
                    throw new Error("Unable to capture database channel object layer details.");
                }

                const data = await response.json();
                setChannel(data);
            } catch (err: any) {
                console.error(err);
                setError(err.message || "An unexpected system execution fault occurred.");
            } finally {
                setLoading(false);
            }
        };

        fetchChannelNode();
    }, [channelId]);

    if (loading) {
        return (
            <div className="min-h-screen bg-white flex flex-col items-center justify-center p-6">
                <div className="h-6 w-6 animate-spin rounded-full border-2 border-gray-900 border-t-transparent" />
                <p className="mt-4 text-xs font-mono text-gray-400 uppercase tracking-widest">Resolving Workspace Node...</p>
            </div>
        );
    }

    if (error || !channel) {
        return (
            <div className="min-h-screen bg-white flex flex-col items-center justify-center p-6 text-center">
                <div className="h-10 w-10 rounded-xl bg-red-50 flex items-center justify-center text-red-600 font-bold mb-4">!</div>
                <h3 className="text-base font-black text-gray-900 tracking-tight">Channel Unreachable</h3>
                <p className="mt-1 text-xs text-gray-500 max-w-sm leading-relaxed">{error}</p>
                <Link href="/channels" className="mt-5 inline-flex h-10 items-center justify-center px-4 bg-gray-900 text-white text-xs font-bold rounded-xl">
                    Return to Directory
                </Link>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50/60 text-gray-900 antialiased font-sans">

            {/* Platform Workspace Navigation Breadcrumb Bar */}
            <header className="border-b border-gray-200 bg-white sticky top-0 z-30 backdrop-blur-md">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <Link href="/pages/channel" className="text-xs font-bold text-gray-500 hover:text-gray-900 transition-colors">
                            &larr; Directory Hub
                        </Link>
                        <span className="text-gray-300 font-mono">/</span>
                        <span className="text-xs font-bold font-mono bg-gray-100 text-gray-700 px-2 py-0.5 rounded border border-gray-200">
                            ID: {channel.channel_id}
                        </span>
                    </div>

                    <div className="flex items-center gap-2">
                        <span className={`inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase tracking-widest border ${channel.visibility === "public" ? "bg-green-50 border-green-200 text-green-700" : "bg-purple-50 border-purple-200 text-purple-700"
                            }`}>
                            {channel.visibility} Node
                        </span>
                    </div>
                </div>
            </header>

            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">

                {/* Profile Card Canvas Container Wrapper */}
                <div className="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden relative">

                    {/* Cover Photo Backdrop Anchor */}
                    <div className="h-44 sm:h-60 md:h-64 w-full bg-gradient-to-r from-gray-200 via-gray-300 to-gray-400 relative">
                        {channel.cover_image && (
                            // eslint-disable-next-line @next/next/no-img-element
                            <img
                                src={`${API_BASE_URL}/${channel.cover_image}`}
                                alt="Channel Workspace Backdrop Banner"
                                className="w-full h-full object-cover"
                            />
                        )}

                        {/* Quick Action Overlap Configuration Control Deck */}
                        <div className="absolute top-4 right-4 flex items-center gap-2 z-20">
                            <button
                                onClick={() => router.push(`/channels/edit/${channel.channel_id}`)}
                                className="inline-flex items-center gap-1.5 h-9 px-3.5 bg-white/95 hover:bg-white text-gray-800 hover:text-gray-950 text-xs font-bold rounded-xl shadow-sm border border-gray-200 transition-all active:scale-95"
                                title="Edit Configuration parameters"
                            >
                                {/* SVG Edit Pencil Icon */}
                                <svg className="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                                </svg>
                                <span>Edit Hub</span>
                            </button>

                            <button
                                className="inline-flex items-center justify-center h-9 w-9 bg-white/95 hover:bg-white text-gray-700 hover:text-gray-950 rounded-xl shadow-sm border border-gray-200 transition-all active:scale-95 group"
                                title="Channel System Security Engine Options"
                            >
                                {/* SVG Gear Settings Icon */}
                                <svg className="h-4 w-4 group-hover:rotate-45 transition-transform duration-300" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2.5">
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                                    <path strokeLinecap="round" strokeLinejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                </svg>
                            </button>
                        </div>
                    </div>

                    {/* Profile Identity Crest Overlay Frame Section */}
                    <div className="px-6 sm:px-8 pb-6 relative flex flex-col md:flex-row md:items-end justify-between gap-4">

                        {/* Absolute Placed Logo Avatar Frame Deck */}
                        <div className="relative -mt-14 sm:-mt-16 h-24 w-24 sm:h-32 sm:w-32 rounded-xl border-4 border-white bg-white shadow-sm overflow-hidden flex-shrink-0 z-10">
                            {channel.logo_image ? (
                                // eslint-disable-next-line @next/next/no-img-element
                                <img
                                    src={`${API_BASE_URL}/${channel.logo_image}`}
                                    alt="Institutional Crest Badge"
                                    className="w-full h-full object-cover"
                                />
                            ) : (
                                <div className="w-full h-full bg-gray-900 text-white font-black text-xl flex items-center justify-center">
                                    {channel.channel_name.substring(0, 2).toUpperCase()}
                                </div>
                            )}
                        </div>

                        {/* Branding Metadata Label Container */}
                        <div className="pt-2 md:pt-4 md:flex-1 md:pl-4">
                            <h1 className="text-xl sm:text-2xl font-black tracking-tight text-gray-900">
                                {channel.channel_name}
                            </h1>
                            <p className="text-xs font-bold text-gray-400 uppercase tracking-widest mt-0.5">
                                {channel.institute_legal_name}
                            </p>

                            <div className="flex flex-wrap items-center gap-x-4 gap-y-2 mt-3 text-xs text-gray-500 font-medium">
                                {channel.physical_corporate_address && (
                                    <span className="flex items-center gap-1">
                                        📍 {channel.physical_corporate_address}
                                    </span>
                                )}
                                <span className="flex items-center gap-1">
                                    👤 Administrator: {channel.institute_owner_full_name}
                                </span>
                            </div>
                        </div>

                        {/* Anchors External Dynamic Grid Footprints */}
                        <div className="flex items-center gap-2 pt-2 md:pt-0 self-start md:self-end">
                            {channel.official_website_link && (
                                <a
                                    href={channel.official_website_link}
                                    target="_blank"
                                    rel="noreferrer"
                                    className="inline-flex h-9 px-4 border border-gray-300 rounded-xl text-xs font-bold text-gray-700 bg-white hover:bg-gray-50 items-center justify-center shadow-sm"
                                >
                                    Domain Page &rarr;
                                </a>
                            )}
                        </div>

                    </div>
                </div>

                {/* Core Double Rail Layout Split Configuration Layout */}
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 mt-8 items-start">

                    {/* Side Rail Column Left: Profile Information Verification Matrices */}
                    <div className="lg:col-span-4 space-y-6">

                        {/* Overview Summary Panel */}
                        <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm">
                            <h4 className="text-[10px] font-black uppercase tracking-widest text-gray-400 mb-3">Mission Statement Summary</h4>
                            <p className="text-xs text-gray-600 leading-relaxed font-medium">
                                {channel.description || "No description parameter properties configured for this deployment asset."}
                            </p>
                        </div>

                        {/* Enrolled Faculty Whitelist Panel */}
                        <div className="bg-white rounded-2xl border border-gray-200 p-6 shadow-sm">
                            <div className="flex items-center justify-between mb-4">
                                <h4 className="text-[10px] font-black uppercase tracking-widest text-gray-400">Personnel Whitelist</h4>
                                <span className="text-[10px] font-mono font-bold bg-gray-100 text-gray-600 px-2 py-0.5 rounded-md">
                                    {channel.co_hosts_and_faculty_members.length} Clearances
                                </span>
                            </div>

                            {channel.co_hosts_and_faculty_members.length > 0 ? (
                                <div className="space-y-1.5 max-h-52 overflow-y-auto pr-1">
                                    {channel.co_hosts_and_faculty_members.map((email, idx) => (
                                        <div key={idx} className="flex items-center gap-2 p-2 bg-gray-50 border border-gray-100 rounded-xl text-xs text-gray-700 font-medium">
                                            <div className="h-5 w-5 bg-gray-900 text-white rounded-md text-[9px] font-mono flex items-center justify-center font-bold uppercase">
                                                {email.substring(0, 1)}
                                            </div>
                                            <span className="truncate flex-1">{email}</span>
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <p className="text-xs text-gray-400 italic">No co-hosts added into runtime scope indices.</p>
                            )}
                        </div>

                    </div>

                    {/* Right Main Column Side: Creative Formal Functional Modules Panels */}
                    <main className="lg:col-span-8 space-y-6">

                        <div className="flex items-center justify-between border-b border-gray-200 pb-4">
                            <div>
                                <h3 className="text-lg font-black tracking-tight text-gray-900">Ecosystem Framework Pools</h3>
                                <p className="text-xs text-gray-500 mt-0.5">Assigned execution streams linked explicitly over this channel reference layer.</p>
                            </div>
                            <button className="h-9 px-4 bg-gray-900 hover:bg-gray-800 text-white text-xs font-bold rounded-xl transition-all shadow-sm active:scale-95">
                                + New Module Setup
                            </button>
                        </div>

                        {/* Formal Modular Display Deck Cards Grid */}
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">

                            {/* Card 1 */}
                            <div className="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm flex flex-col justify-between group hover:border-gray-300 transition-all">
                                <div>
                                    <div className="flex items-center justify-between mb-3">
                                        <span className="text-[9px] font-black font-mono uppercase tracking-widest px-2 py-0.5 bg-blue-50 text-blue-700 border border-blue-100 rounded">
                                            Core Stream A
                                        </span>
                                        <span className="text-[11px] text-gray-400 font-medium">6 Assignments</span>
                                    </div>
                                    <h4 className="font-bold text-gray-900 text-sm tracking-tight group-hover:text-blue-600 transition-colors">
                                        Advanced Microservices Infrastructure & SOA Systems
                                    </h4>
                                    <p className="text-xs text-gray-400 mt-1 line-clamp-2 leading-relaxed">
                                        Integration structures testing Catalog SOAP boundaries and secure REST Orders routing engines.
                                    </p>
                                </div>
                                <div className="pt-4 mt-4 border-t border-gray-100 flex items-center justify-end text-xs font-bold text-gray-900">
                                    <span>Enter Dashboard &rarr;</span>
                                </div>
                            </div>

                            {/* Card 2 */}
                            <div className="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm flex flex-col justify-between group hover:border-gray-300 transition-all">
                                <div>
                                    <div className="flex items-center justify-between mb-3">
                                        <span className="text-[9px] font-black font-mono uppercase tracking-widest px-2 py-0.5 bg-amber-50 text-amber-700 border border-amber-100 rounded">
                                            Lab Track B
                                        </span>
                                        <span className="text-[11px] text-gray-400 font-medium">Active Research</span>
                                    </div>
                                    <h4 className="font-bold text-gray-900 text-sm tracking-tight group-hover:text-amber-600 transition-colors">
                                        Bioacoustic Classification & Digital Signal Audio Models
                                    </h4>
                                    <p className="text-xs text-gray-400 mt-1 line-clamp-2 leading-relaxed">
                                        Acoustic classification architectures deploying real-time parsing pipelines and Explainable AI indicators.
                                    </p>
                                </div>
                                <div className="pt-4 mt-4 border-t border-gray-100 flex items-center justify-end text-xs font-bold text-gray-900">
                                    <span>Enter Dashboard &rarr;</span>
                                </div>
                            </div>

                        </div>

                    </main>

                </div>

            </div>
        </div>
    );
}