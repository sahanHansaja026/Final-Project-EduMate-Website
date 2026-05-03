"use client";

import { useEffect, useState } from "react";
import { API_BASE_URL } from "@/app/config/api";

type Content = {
    id: number;
    title: string;
    description?: string;
    week: number;
    open_date?: string;
    close_date?: string;
};

type Props = {
    moduleId: string;
};

export default function WeekItemInfo({ moduleId }: Props) {
    const [contents, setContents] = useState<Content[]>([]);
    const [loading, setLoading] = useState(true);
    const [expanded, setExpanded] = useState<Record<string, boolean>>({});
    const [done, setDone] = useState<Record<string, boolean>>({});

    useEffect(() => {
        const fetchContent = async () => {
            try {
                const res = await fetch(`${API_BASE_URL}/contents/module/${moduleId}`);
                if (!res.ok) throw new Error("Failed to fetch content");
                const data = await res.json();
                setContents(data);

                // Load progress from localStorage
                const savedDone = localStorage.getItem(`done_module_${moduleId}`);
                if (savedDone) {
                    setDone(JSON.parse(savedDone));
                }
            } catch (error) {
                console.error("Fetch Error:", error);
            } finally {
                setLoading(false);
            }
        };

        fetchContent();
    }, [moduleId]);

    // Save progress to localStorage
    useEffect(() => {
        if (!loading) {
            localStorage.setItem(`done_module_${moduleId}`, JSON.stringify(done));
        }
    }, [done, moduleId, loading]);

    const today = new Date();

    const getStatus = (item: Content) => {
        if (!item.open_date) return "locked";
        const open = new Date(item.open_date);
        const close = item.close_date ? new Date(item.close_date) : null;

        if (today < open) return "locked";
        if (close && today > close) return "closed";
        return "active";
    };

    const toggleState = (setter: React.Dispatch<React.SetStateAction<Record<string, boolean>>>, key: string) => {
        setter((prev) => ({
            ...prev,
            [key]: !prev[key],
        }));
    };

    // --- FILTERING LOGIC ---
    // This ensures that "Locked" items do not appear in the UI at all.
    const visibleContents = contents.filter((item) => getStatus(item) !== "locked");

    return (
        <div className="space-y-6">
            {loading ? (
                <div className="text-gray-400 text-sm animate-pulse">Loading content...</div>
            ) : visibleContents.length === 0 ? (
                <div className="text-gray-400 text-sm italic border-2 border-dashed p-4 rounded-xl text-center">
                    No active content available at this time.
                </div>
            ) : (
                visibleContents.map((item, index) => {
                    const status = getStatus(item);
                    // Guaranteed unique key for state tracking
                    const itemKey = `content-${item.id}-${index}`;
                    const isDone = !!done[itemKey];
                    const isExpanded = !!expanded[itemKey];

                    return (
                        <div
                            key={itemKey}
                            className={`flex gap-4 p-5 border rounded-2xl transition-all ${
                                status === "active"
                                    ? "bg-white border-gray-100 shadow-sm"
                                    : "bg-gray-50 border-transparent opacity-70"
                            }`}
                        >
                            {/* STATUS INDICATOR */}
                            <div className="flex flex-col items-center mt-1">
                                <div
                                    className={`w-4 h-4 rounded-full border-2 ${
                                        isDone 
                                            ? "bg-green-500 border-green-200" 
                                            : "bg-blue-500 border-blue-100"
                                    }`}
                                />
                                <div className="w-[2px] flex-1 bg-gray-100 mt-2" />
                            </div>

                            {/* TEXT CONTENT */}
                            <div className="flex-1">
                                <div className="flex items-start justify-between gap-4">
                                    <div>
                                        <h4 className={`text-base font-bold ${
                                            isDone ? "text-gray-400 line-through" : "text-gray-800"
                                        }`}>
                                            {item.title}
                                        </h4>
                                        
                                        {status === "closed" && (
                                            <span className="text-[10px] font-bold text-red-400 uppercase tracking-tight">
                                                ⛔ Access Expired
                                            </span>
                                        )}
                                    </div>

                                    <button
                                        onClick={() => toggleState(setDone, itemKey)}
                                        disabled={status !== "active"}
                                        className={`shrink-0 text-xs font-bold px-4 py-2 rounded-xl border-2 transition-all ${
                                            isDone
                                                ? "bg-green-500 border-green-500 text-white"
                                                : status === "active"
                                                ? "bg-white border-gray-200 text-gray-700 hover:border-blue-500"
                                                : "bg-gray-100 border-gray-100 text-gray-400 cursor-not-allowed"
                                        }`}
                                    >
                                        {isDone ? "Done ✓" : "Mark Done"}
                                    </button>
                                </div>

                                {status === "active" && item.description && (
                                    <div className="mt-3">
                                        <p className="text-sm text-gray-500 leading-relaxed">
                                            {isExpanded || item.description.length <= 120
                                                ? item.description
                                                : `${item.description.slice(0, 120)}...`}
                                            
                                            {item.description.length > 120 && (
                                                <button
                                                    onClick={() => toggleState(setExpanded, itemKey)}
                                                    className="ml-2 text-blue-500 font-bold hover:underline"
                                                >
                                                    {isExpanded ? "Less" : "More"}
                                                </button>
                                            )}
                                        </p>
                                    </div>
                                )}
                            </div>
                        </div>
                    );
                })
            )}
        </div>
    );
}