"use client";

import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { getUser } from "@/app/services/authService";
import { API_BASE_URL } from "@/app/config/api";

type Subscription = {
    subscription_type: "free" | "pro" | "edu_pro";
    video_limit: number | "unlimited";
    module_limit: number | "unlimited";
    quiz_limit: number | "unlimited";
    channel_limit: number | "unlimited";
};

export default function SubscriptionPage() {
    const searchParams = useSearchParams();
    const reason = searchParams.get("reason");

    const [user, setUser] = useState<{ id: number; email: string } | null>(null);
    const [subscription, setSubscription] = useState<Subscription | null>(null);
    const [isLoading, setIsLoading] = useState<string | null>(null); // Track which plan is updating

    const currentPlan = subscription?.subscription_type ?? "free";

    useEffect(() => {
        setUser(getUser());
    }, []);

    // Encapsulated load function so it can be re-called after updates
    const fetchSubscription = async (userId: number) => {
        try {
            const res = await fetch(`${API_BASE_URL}/subscription/${userId}`);
            if (!res.ok) throw new Error("Failed to load subscription");
            const data = await res.json();
            setSubscription(data);
        } catch (err) {
            console.error("Error fetching subscription:", err);
        }
    };

    useEffect(() => {
        if (user) {
            fetchSubscription(user.id);
        }
    }, [user]);

    // HANDLER TO UPDATE PLAN ON BACKEND
    const handlePlanUpdate = async (targetPlan: "free" | "pro" | "edu_pro") => {
        if (!user) return alert("You must be logged in to modify your subscription.");

        setIsLoading(targetPlan);

        try {
            // Since FastAPI expects Form data, we use URLSearchParams
            const formData = new URLSearchParams();
            formData.append("subscription_type", targetPlan);
            formData.append("status", "active");

            const res = await fetch(`${API_BASE_URL}/subscription/update/${user.id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
                body: formData.toString(),
            });

            if (!res.ok) {
                const errorData = await res.json();
                throw new Error(errorData.detail || "Failed to update subscription");
            }

            // Refresh user subscription data locally on success
            await fetchSubscription(user.id);
            alert(`Subscription successfully provisioned to ${targetPlan.toUpperCase()}`);

        } catch (err: any) {
            console.error("Update error:", err);
            alert(`Provisioning failed: ${err.message}`);
        } finally {
            setIsLoading(null);
        }
    };

    return (
        <div className="min-h-screen bg-slate-100 text-slate-800 flex flex-col justify-between p-6 md:p-12 font-sans">
            <div className="w-full max-w-6xl mx-auto bg-white rounded-xl shadow-md border border-slate-200 overflow-hidden">

                {/* ACADEMIC HEADER */}
                <div className="bg-slate-900 text-white p-8 border-b border-slate-800">
                    <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                        <div>
                            <span className="text-xs font-semibold tracking-wider uppercase text-indigo-400">
                                Institutional Access & Licensing
                            </span>
                            <h1 className="text-3xl font-serif font-bold tracking-tight mt-1">
                                Academic Tier Management
                            </h1>
                            <p className="text-sm text-slate-400 mt-2 max-w-2xl">
                                Review your current learning parameters or provision advanced LMS features for classrooms and higher education workflows.
                            </p>
                        </div>

                        {/* CURRENT STATUS BADGE */}
                        <div className="bg-slate-800 border border-slate-700 px-5 py-3 rounded-lg flex flex-col justify-center">
                            <span className="text-xs text-slate-400 font-medium uppercase tracking-wider">Active Workspace</span>
                            <span className="text-lg font-semibold text-slate-100 capitalize mt-0.5">
                                {currentPlan === "edu_pro" ? "🏫 Edu Pro Institutional" : currentPlan === "pro" ? "🚀 Professional Tier" : "Standard (Free)"}
                            </span>
                        </div>
                    </div>

                    {/* DYNAMIC SYSTEM ALERT */}
                    {reason && (
                        <div className="mt-6 p-4 bg-amber-500/10 border border-amber-500/30 text-amber-300 text-sm rounded-lg flex items-center gap-2">
                            <span className="font-bold">System Notice:</span>
                            <span>Action required. Access to resource was paused due to standard tier thresholds ({reason}). Please update allocation below.</span>
                        </div>
                    )}
                </div>

                <div className="p-8">
                    {/* SECTION TITLE */}
                    <div className="mb-6 pb-4 border-b border-slate-200">
                        <h2 className="text-lg font-semibold text-slate-700">Available Account Allocations</h2>
                        <p className="text-xs text-slate-500">Configure your limits, content delivery modules, and evaluation tools.</p>
                    </div>

                    {/* TIERS GRID */}
                    <div className="grid lg:grid-cols-3 gap-6 items-stretch">

                        {/* STANDARD TIER */}
                        <div className={`flex flex-col justify-between p-6 rounded-xl border transition-all ${currentPlan === "free" ? "border-slate-400 bg-slate-50/50 ring-1 ring-slate-400" : "border-slate-200 bg-white"}`}>
                            <div>
                                <div className="flex justify-between items-start">
                                    <div>
                                        <h3 className="text-lg font-bold text-slate-900">Standard Tier</h3>
                                        <p className="text-xs text-slate-500 mt-1">Independent self-study environments</p>
                                    </div>
                                    {currentPlan === "free" && (
                                        <span className="text-xs px-2 py-1 bg-slate-200 text-slate-700 font-medium rounded">Current</span>
                                    )}
                                </div>

                                <div className="mt-6 space-y-4">
                                    <div>
                                        <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Curriculum Limits</h4>
                                        <ul className="text-sm space-y-2 text-slate-600">
                                            <li className="flex items-center gap-2">▪ 1 Curated Module</li>
                                            <li className="flex items-center gap-2">▪ 1 Media Stream / Video</li>
                                            <li className="flex items-center gap-2">▪ 5 Core Learning Objects</li>
                                        </ul>
                                    </div>
                                    <div>
                                        <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Evaluation Metrics</h4>
                                        <ul className="text-sm space-y-2 text-slate-600">
                                            <li className="flex items-center gap-2">▪ 3 Examination Quizzes</li>
                                            <li className="flex items-center gap-2">▪ 2 Student Assignments</li>
                                            <li className="flex items-center gap-2">▪ 1 Public Discovery Channel</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>

                            <button
                                onClick={() => handlePlanUpdate("free")}
                                disabled={currentPlan === "free" || isLoading !== null}
                                className={`mt-8 w-full py-2.5 text-sm font-medium rounded-lg border transition-colors ${currentPlan === "free"
                                        ? "bg-slate-100 text-slate-400 border-slate-200 cursor-not-allowed"
                                        : "bg-white text-slate-600 border-slate-300 hover:bg-slate-50"
                                    }`}
                            >
                                {isLoading === "free" ? "Processing..." : currentPlan === "free" ? "Your Active Tier" : "Revert Allocation"}
                            </button>
                        </div>

                        {/* PROFESSIONAL TIER */}
                        <div className={`flex flex-col justify-between p-6 rounded-xl border transition-all ${currentPlan === "pro" ? "border-indigo-600 bg-indigo-50/20 ring-1 ring-indigo-600" : "border-slate-200 bg-white"}`}>
                            <div>
                                <div className="flex justify-between items-start">
                                    <div>
                                        <h3 className="text-lg font-bold text-indigo-900">Professional Educator</h3>
                                        <p className="text-xs text-indigo-600 mt-1">For single-classroom instructors & independent creators</p>
                                    </div>
                                    {currentPlan === "pro" && (
                                        <span className="text-xs px-2 py-1 bg-indigo-600 text-white font-medium rounded">Current</span>
                                    )}
                                </div>

                                <div className="mt-6 space-y-4">
                                    <div>
                                        <h4 className="text-xs font-semibold text-indigo-400 uppercase tracking-wider mb-2">Curriculum Limits</h4>
                                        <ul className="text-sm space-y-2 text-slate-700">
                                            <li className="flex items-center gap-2 font-medium text-slate-900">✓ Unlimited Course Modules</li>
                                            <li className="flex items-center gap-2 font-medium text-slate-900">✓ Unlimited Video Deployments</li>
                                            <li className="flex items-center gap-2 font-medium text-slate-900">✓ Unlimited Content Nodes</li>
                                        </ul>
                                    </div>
                                    <div>
                                        <h4 className="text-xs font-semibold text-indigo-400 uppercase tracking-wider mb-2">Evaluation Metrics</h4>
                                        <ul className="text-sm space-y-2 text-slate-700">
                                            <li className="flex items-center gap-2">✓ Unlimited Quizzes & Question Banks</li>
                                            <li className="flex items-center gap-2">✓ Unlimited Graded Assignments</li>
                                            <li className="flex items-center gap-2">✓ Expanded Instructor Channels</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>

                            <button
                                onClick={() => handlePlanUpdate("pro")}
                                disabled={currentPlan === "pro" || isLoading !== null}
                                className={`mt-8 w-full py-2.5 text-sm font-semibold rounded-lg transition-colors ${currentPlan === "pro"
                                        ? "bg-slate-100 text-slate-400 border border-slate-200 cursor-not-allowed"
                                        : "bg-indigo-600 text-white hover:bg-indigo-700 shadow-sm"
                                    }`}
                            >
                                {isLoading === "pro" ? "Processing..." : currentPlan === "pro" ? "Your Active Tier" : "Provision Professional Access"}
                            </button>
                        </div>

                        {/* EDU PRO TIER */}
                        <div className={`flex flex-col justify-between p-6 rounded-xl border transition-all ${currentPlan === "edu_pro" ? "border-emerald-600 bg-emerald-50/20 ring-1 ring-emerald-600" : "border-slate-200 bg-white"}`}>
                            <div>
                                <div className="flex justify-between items-start">
                                    <div>
                                        <h3 className="text-lg font-bold text-emerald-900">LMS Institutional (Edu Pro)</h3>
                                        <p className="text-xs text-emerald-700 mt-1">Multi-seat licenses for schools, faculties & universities</p>
                                    </div>
                                    {currentPlan === "edu_pro" && (
                                        <span className="text-xs px-2 py-1 bg-emerald-600 text-white font-medium rounded">Current</span>
                                    )}
                                </div>

                                <div className="mt-6 space-y-4">
                                    <div>
                                        <h4 className="text-xs font-semibold text-emerald-600/70 uppercase tracking-wider mb-2">Campus Administration</h4>
                                        <ul className="text-sm space-y-2 text-slate-700">
                                            <li className="flex items-center gap-2 font-medium text-emerald-950">🏛 Unified Central LMS Dashboard</li>
                                            <li className="flex items-center gap-2 font-medium text-emerald-950">🏛 Hierarchical Roles (Admin, Teacher, Student)</li>
                                            <li className="flex items-center gap-2 font-medium text-emerald-950">🏛 Campus-wide Course Provisioning Tools</li>
                                        </ul>
                                    </div>
                                    <div>
                                        <h4 className="text-xs font-semibold text-emerald-600/70 uppercase tracking-wider mb-2">Academic Operations</h4>
                                        <ul className="text-sm space-y-2 text-slate-700">
                                            <li className="flex items-center gap-2">✓ Global Resource Catalogs</li>
                                            <li className="flex items-center gap-2">✓ Inter-departmental Content Synced tools</li>
                                            <li className="flex items-center gap-2">✓ Institutional Cohort Analytics</li>
                                        </ul>
                                    </div>
                                </div>
                            </div>

                            <button
                                onClick={() => handlePlanUpdate("edu_pro")}
                                disabled={currentPlan === "edu_pro" || isLoading !== null}
                                className={`mt-8 w-full py-2.5 text-sm font-semibold rounded-lg transition-colors ${currentPlan === "edu_pro"
                                        ? "bg-slate-100 text-slate-400 border border-slate-200 cursor-not-allowed"
                                        : "bg-emerald-700 text-white hover:bg-emerald-800 shadow-sm"
                                    }`}
                            >
                                {isLoading === "edu_pro" ? "Processing..." : currentPlan === "edu_pro" ? "Your Active Tier" : "Request Campus-wide License"}
                            </button>
                        </div>

                    </div>
                </div>
            </div>

            {/* INSTITUTIONAL FOOTER */}
            <footer className="mt-8 text-center text-xs text-slate-500 max-w-xl mx-auto space-y-1">
                <p>FERPA / GDPR Compliant Enterprise LMS Protocol Architecture.</p>
                <p className="text-slate-400">For custom enterprise deployments or API integrations, contact your district's systems administrator.</p>
            </footer>
        </div>
    );
}