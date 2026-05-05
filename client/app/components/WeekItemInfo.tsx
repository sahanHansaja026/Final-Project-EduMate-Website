"use client";

import { useEffect, useState } from "react";
import { API_BASE_URL } from "@/app/config/api";
import { getUser } from "../services/authService";
import Link from "next/link"; // Added for navigation

type Content = {
    assignment_id: number; // ✅ FIXED (important)
    title: string;
    description?: string;
    week: number;
    open_date?: string;
    close_date?: string;
};

type Module = {
    module_id: number;
    user_id: number;
    name: string;
    description?: string;
};

type Props = {
    moduleId: string;
};

export default function WeekItemInfo({ moduleId }: Props) {
    const [contents, setContents] = useState<Content[]>([]);
    const [module, setModule] = useState<Module | null>(null);
    const [loading, setLoading] = useState(true);
    const [expanded, setExpanded] = useState<Record<string, boolean>>({});
    const [done, setDone] = useState<Record<string, boolean>>({});
    const [user, setUser] = useState<{ id: number; email: string } | null>(null);

    useEffect(() => {
        const currentUser = getUser();
        setUser(currentUser);
    }, []);

    const fetchData = async () => {
        try {
            const moduleRes = await fetch(`${API_BASE_URL}/modules/${moduleId}`);
            if (!moduleRes.ok) throw new Error("Failed to fetch module");
            const moduleData = await moduleRes.json();
            setModule(moduleData);

            const contentRes = await fetch(`${API_BASE_URL}/contents/module/${moduleId}`);
            if (!contentRes.ok) throw new Error("Failed to fetch content");
            const contentData = await contentRes.json();
            setContents(contentData);

            const savedDone = localStorage.getItem(`done_module_${moduleId}`);
            if (savedDone) setDone(JSON.parse(savedDone));
        } catch (error) {
            console.error("Fetch Error:", error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, [moduleId]);

    useEffect(() => {
        if (!loading) {
            localStorage.setItem(`done_module_${moduleId}`, JSON.stringify(done));
        }
    }, [done, moduleId, loading]);

    // 👉 NEW: DELETE HANDLER
    const handleDelete = async (contentId: number) => {
        const confirmed = window.confirm("Are you sure you want to delete this activity?");
        if (!confirmed) return;

        try {
            const res = await fetch(`${API_BASE_URL}/contents/${contentId}`, {
                method: "DELETE",
            });

            if (res.ok) {
                // Update local state to remove the item immediately
                setContents((prev) => prev.filter((c) => c.assignment_id !== contentId));
            } else {
                alert("Failed to delete the item. Please try again.");
            }
        } catch (error) {
            console.error("Delete error:", error);
            alert("An error occurred while deleting.");
        }
    };

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
        setter((prev) => ({ ...prev, [key]: !prev[key] }));
    };

    const isOwner = user?.id === module?.user_id;

    const visibleContents = isOwner
        ? contents
        : contents.filter((item) => getStatus(item) !== "locked");

    return (
        <div className="space-y-6">
            {loading ? (
                <div className="text-gray-400 text-sm animate-pulse">Loading content...</div>
            ) : visibleContents.length === 0 ? (
                <div className="text-gray-400 text-sm italic border-2 border-dashed p-4 rounded-xl text-center">No content available.</div>
            ) : (
                visibleContents.map((item, index) => {
                    const status = getStatus(item);
                    const itemKey = `content-${item.assignment_id}-${index}`;
                    const isDone = !!done[itemKey];
                    const isExpanded = !!expanded[itemKey];

                    return (
                        <div key={itemKey} className={`flex gap-4 p-5 border rounded-2xl transition-all ${status === "active" ? "bg-white border-gray-100 shadow-sm" : "bg-gray-50 border-transparent opacity-70"}`}>
                            <div className="flex flex-col items-center mt-1">
                                <div className={`w-4 h-4 rounded-full border-2 ${isDone ? "bg-green-500 border-green-200" : "bg-blue-500 border-blue-100"}`} />
                                <div className="w-[2px] flex-1 bg-gray-100 mt-2" />
                            </div>

                            <div className="flex-1">
                                <div className="flex items-start justify-between gap-4">
                                    <div>
                                        <h4 className={`text-base font-bold ${isDone ? "text-gray-400 line-through" : "text-gray-800"}`}>
                                            {item.title}
                                            {isOwner && (
                                                <span className="ml-2 text-[10px] text-blue-500 bg-blue-50 px-2 py-0.5 rounded uppercase font-mono">
                                                    Owner Mode ({status})
                                                </span>
                                            )}
                                        </h4>
                                        {status === "closed" && !isOwner && (
                                            <span className="text-[10px] font-bold text-red-400 uppercase">⛔ Access Expired</span>
                                        )}
                                    </div>

                                    <div className="flex items-center gap-2">
                                        {isOwner && (
                                            <div className="flex items-center gap-2 mr-2 border-r pr-2 border-gray-200">
                                                {/* EDIT BUTTON */}
                                                <Link
                                                    href={`/pages/content/edit/${item.assignment_id}`}
                                                    className="text-xs font-bold px-3 py-1.5 rounded-lg bg-yellow-100 text-yellow-700 hover:bg-yellow-200 transition-colors"
                                                >
                                                    Edit
                                                </Link>

                                                {/* DELETE BUTTON */}
                                                <button
                                                    onClick={() => handleDelete(item.assignment_id)}
                                                    className="text-xs font-bold px-3 py-1.5 rounded-lg bg-red-100 text-red-600 hover:bg-red-200 transition-colors"
                                                >
                                                    Delete
                                                </button>

                                                {/* GRADE BUTTON (UNTOUCHED) */}
                                                <button
                                                    onClick={() => console.log("Grade", item.assignment_id)}
                                                    className="text-xs font-bold px-3 py-1.5 rounded-lg bg-purple-100 text-purple-700 hover:bg-purple-200 transition-colors"
                                                >
                                                    Grade
                                                </button>
                                            </div>
                                        )}

                                        <button
                                            onClick={() => toggleState(setDone, itemKey)}
                                            disabled={status !== "active" && !isOwner}
                                            className={`text-xs font-bold px-4 py-2 rounded-xl border-2 transition-all ${isDone ? "bg-green-500 border-green-500 text-white" : status === "active" || isOwner ? "bg-white border-gray-200 text-gray-700 hover:border-blue-500 hover:text-blue-500" : "bg-gray-100 text-gray-400 cursor-not-allowed"}`}
                                        >
                                            {isDone ? "Done ✓" : "Mark Done"}
                                        </button>
                                    </div>
                                </div>

                                {item.description && (
                                    <div className="mt-3">
                                        <p className="text-sm text-gray-500 leading-relaxed">
                                            {isExpanded || item.description.length <= 120 ? item.description : `${item.description.slice(0, 120)}...`}
                                            {item.description.length > 120 && (
                                                <button onClick={() => toggleState(setExpanded, itemKey)} className="ml-2 text-blue-500 font-bold hover:underline">
                                                    {isExpanded ? "Show Less" : "Read More"}
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