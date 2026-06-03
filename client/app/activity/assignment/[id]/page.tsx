"use client";

import { useEffect, useState, useCallback } from "react";
import { useParams } from "next/navigation";
import { API_BASE_URL } from "@/app/config/api";
import { getUser } from "@/app/services/authService";
import Link from "next/link";
import {
    Calendar,
    Clock,
    FileText,
    Download,
    UploadCloud,
    CheckCircle2,
    AlertCircle,
    Loader2,
    ArrowLeft,
    MessageSquare,
    User,
} from "lucide-react";

type Assignment = {
    id: number;
    module_id: number;
    title: string;
    description: string;
    file_path: string | null;
    open_date: string | null;
    close_date: string | null;
    allow_download: boolean;
};

export default function Page() {
    const params = useParams();
    const id = params.id as string;

    const [assignment, setAssignment] = useState<Assignment | null>(null);
    const [loading, setLoading] = useState(true);
    const [user, setUser] = useState<any>(null);

    // submission UI panel states
    const [isFormOpen, setIsFormOpen] = useState(false);

    // submission data states
    const [file, setFile] = useState<File | null>(null);
    const [customName, setCustomName] = useState("");
    const [feedback, setFeedback] = useState("");
    const [submitting, setSubmitting] = useState(false);
    const [submission, setSubmission] = useState<any>(null);
    const [checking, setChecking] = useState(true);

    useEffect(() => {
        const u = getUser();
        setUser(u);
    }, []);

    useEffect(() => {
        const fetchAssignment = async () => {
            try {
                const res = await fetch(`${API_BASE_URL}/assignments/${id}`);
                if (!res.ok) {
                    setAssignment(null);
                    return;
                }
                const data = await res.json();
                setAssignment(data);
            } catch (err) {
                console.error(err);
                setAssignment(null);
            } finally {
                setLoading(false);
            }
        };

        fetchAssignment();
    }, [id]);

    const fetchSubmission = useCallback(async () => {
        if (!user?.id) return;
        try {
            setChecking(true);
            const res = await fetch(
                `${API_BASE_URL}/submissions/check/${id}/${user.id}`
            );

            if (!res.ok) {
                setSubmission(null);
                return;
            }

            const data = await res.json();
            setSubmission(data);
        } catch (err) {
            console.error(err);
            setSubmission(null);
        } finally {
            setChecking(false);
        }
    }, [id, user?.id]);

    useEffect(() => {
        fetchSubmission();
    }, [fetchSubmission]);

    const handleCancel = () => {
        setFile(null);
        setCustomName("");
        setFeedback("");
        setIsFormOpen(false);
    };

    const handleSubmit = async () => {
        if (!user?.id) {
            alert("Please login first");
            return;
        }

        if (!file) {
            alert("Please select a file");
            return;
        }

        try {
            setSubmitting(true);
            const formData = new FormData();
            formData.append("assignment_id", id);
            formData.append("student_id", user.id);

            const renamedFile = new File(
                [file],
                customName || file.name,
                { type: file.type }
            );
            formData.append("file", renamedFile);

            const res = await fetch(`${API_BASE_URL}/submissions/`, {
                method: "POST",
                body: formData,
            });

            if (!res.ok) {
                throw new Error("Submission failed");
            }

            alert("Assignment submitted successfully!");
            handleCancel();
            await fetchSubmission();
        } catch (err) {
            console.error(err);
            alert("Error submitting assignment");
        } finally {
            setSubmitting(false);
        }
    };

    if (loading) {
        return (
            <div className="max-w-4xl mx-auto p-12 flex flex-col items-center justify-center space-y-4 text-slate-500">
                <Loader2 className="h-8 w-8 animate-spin text-blue-600" />
                <span className="text-sm font-medium tracking-wide">Loading assignment workspace...</span>
            </div>
        );
    }

    if (!assignment) {
        return (
            <div className="max-w-4xl mx-auto p-6">
                <div className="bg-red-50 border border-red-200 text-red-800 p-4 rounded-xl flex items-start gap-3 text-sm">
                    <AlertCircle className="h-5 w-5 text-red-600 mt-0.5 flex-shrink-0" />
                    <div>
                        <h4 className="font-semibold">Assignment Unavailable</h4>
                        <p className="text-red-700/90 mt-0.5">The resource you are looking for does not exist or has been archived by the instructor.</p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="max-w-4xl mx-auto p-6 space-y-6 bg-slate-50/50 min-h-screen">

            {/* BREADCRUMB / TOP NAVIGATION */}
            <div className="flex items-center justify-between text-xs text-slate-500 tracking-wide uppercase font-semibold">
                <Link href={`/moduleinside/${assignment.module_id}`}>
                <button className="flex items-center gap-1.5 hover:text-slate-800 transition">
                    <ArrowLeft className="h-3.5 w-3.5" /> Back to Course
                </button>
            </Link>
                <div className="flex items-center gap-1.5 bg-slate-100 px-2.5 py-1 rounded text-slate-600">
                    <User className="h-3 w-3" /> {user ? `ID: ${user.id}` : "Guest Access"}
                </div>
            </div>

            {/* ASSIGNMENT HEADER & DETAILS */}
            <article className="bg-white border border-slate-200/80 rounded-xl p-6 shadow-sm">
                <div className="space-y-1">
                    <span className="text-xs font-bold text-blue-600 tracking-wider uppercase">Course Assignment</span>
                    <h1 className="text-2xl font-bold text-slate-900 tracking-tight">
                        {assignment.title}
                    </h1>
                </div>

                {/* Academic Metadata Grid */}
                <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-3 bg-slate-50 p-3.5 rounded-lg border border-slate-100 text-sm">
                    <div className="flex items-center gap-2.5 text-slate-600">
                        <Calendar className="h-4 w-4 text-slate-400" />
                        <span><strong className="text-slate-500 font-medium">Open Date:</strong> {assignment.open_date ? new Date(assignment.open_date).toLocaleString() : "Immediate"}</span>
                    </div>
                    <div className="flex items-center gap-2.5 text-slate-600">
                        <Clock className="h-4 w-4 text-slate-400" />
                        <span><strong className="text-slate-500 font-medium">Due Date:</strong> {assignment.close_date ? new Date(assignment.close_date).toLocaleString() : "No Deadline"}</span>
                    </div>
                </div>

                <div className="mt-6">
                    <h3 className="text-xs font-bold text-slate-400 tracking-wider uppercase mb-2">Instructions</h3>
                    <p className="text-slate-700 leading-relaxed whitespace-pre-wrap text-sm border-l-2 border-slate-200 pl-4">
                        {assignment.description}
                    </p>
                </div>

                {assignment.file_path && (
                    <div className="mt-6 pt-4 border-t border-slate-100">
                        <a
                            href={`${API_BASE_URL}/${assignment.file_path}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-2 bg-slate-900 hover:bg-slate-800 text-xs font-semibold text-white px-4 py-2.5 rounded-lg transition shadow-sm"
                        >
                            <Download className="h-3.5 w-3.5" /> Download Reference Material
                        </a>
                    </div>
                )}
            </article>

            {/* SUBMISSION BLOCK */}
            <section className="bg-white border border-slate-200/80 rounded-xl p-6 shadow-sm space-y-6">
                <div className="border-b border-slate-100 pb-3 flex items-center justify-between">
                    <h2 className="text-base font-bold text-slate-900 tracking-tight">
                        Submission Status
                    </h2>
                </div>

                {checking ? (
                    <div className="flex items-center gap-2 text-sm text-slate-400 py-2">
                        <Loader2 className="h-4 w-4 animate-spin text-slate-400" />
                        Checking institutional records...
                    </div>
                ) : submission ? (
                    /* GRADED / SUBMITTED BLOCK */
                    <div className="space-y-5">
                        <div className={`p-4 rounded-xl border flex flex-col sm:flex-row sm:items-center justify-between gap-4 ${submission.marks !== null
                                ? "bg-emerald-50/60 border-emerald-200/70 text-emerald-900"
                                : "bg-blue-50/60 border-blue-200/70 text-blue-900"
                            }`}>
                            <div className="flex items-start gap-3">
                                <CheckCircle2 className={`h-5 w-5 mt-0.5 ${submission.marks !== null ? "text-emerald-600" : "text-blue-600"}`} />
                                <div>
                                    <span className="font-bold text-xs uppercase tracking-wider block">
                                        {submission.marks !== null ? "Evaluation Complete" : "Successfully Received"}
                                    </span>
                                    <p className="text-xs opacity-80 mt-0.5">
                                        Recorded timestamp: {new Date(submission.submitted_at).toLocaleString()}
                                    </p>
                                </div>
                            </div>
                            {submission.marks !== null && (
                                <div className="bg-white border border-emerald-200 px-4 py-2 rounded-lg text-center shadow-sm min-w-[100px]">
                                    <span className="text-[10px] uppercase font-bold tracking-wider text-slate-400 block">Grade Score</span>
                                    <span className="text-2xl font-black text-emerald-700">{submission.marks}</span>
                                </div>
                            )}
                        </div>

                        {/* Submission Details Table View */}
                        <div className="border border-slate-200 rounded-xl overflow-hidden text-sm bg-white">
                            <table className="w-full text-left border-collapse">
                                <tbody>
                                    <tr className="border-b border-slate-100 bg-slate-50/40">
                                        <td className="p-3.5 font-semibold text-slate-500 w-1/3 text-xs uppercase tracking-wider">Submitted Document</td>
                                        <td className="p-3.5">
                                            <a
                                                className="text-blue-600 hover:text-blue-800 font-medium inline-flex items-center gap-1.5 underline underline-offset-4"
                                                href={`${API_BASE_URL}/${submission.file_path}`}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                            >
                                                <FileText className="h-4 w-4" /> View File Receipt
                                            </a>
                                        </td>
                                    </tr>
                                    {submission.feedback && (
                                        <tr>
                                            <td className="p-3.5 font-semibold text-slate-500 align-top text-xs uppercase tracking-wider">Instructor Assessment Remarks</td>
                                            <td className="p-3.5 text-slate-700 whitespace-pre-wrap bg-slate-50/20 text-xs sm:text-sm leading-relaxed">
                                                <div className="flex gap-2 items-start">
                                                    <MessageSquare className="h-4 w-4 text-slate-400 mt-0.5 flex-shrink-0" />
                                                    <p>{submission.feedback}</p>
                                                </div>
                                            </td>
                                        </tr>
                                    )}
                                </tbody>
                            </table>
                        </div>
                    </div>
                ) : (
                    /* NOT SUBMITTED STATE */
                    <div className="space-y-4">
                        <div className="bg-amber-50/70 border border-amber-200/80 text-amber-900 p-4 rounded-xl flex items-start gap-3 text-sm">
                            <AlertCircle className="h-5 w-5 text-amber-600 mt-0.5 flex-shrink-0" />
                            <div>
                                <h4 className="font-semibold">No Record Found</h4>
                                <p className="text-amber-800/90 mt-0.5">You have not submitted any materials for this evaluation task yet.</p>
                            </div>
                        </div>

                        {!user && (
                            <p className="text-xs text-red-600 font-semibold flex items-center gap-1.5 bg-red-50 p-2.5 rounded-lg border border-red-100">
                                <AlertCircle className="h-4 w-4" /> Authentication missing. Please authenticate through your student portal dashboard.
                            </p>
                        )}

                        {user && !isFormOpen && (
                            <button
                                onClick={() => setIsFormOpen(true)}
                                className="bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs uppercase tracking-wider px-5 py-3 rounded-lg transition shadow-sm"
                            >
                                Open Submission Panel
                            </button>
                        )}
                    </div>
                )}

                {/* EXPANDABLE SUBMISSION FORM */}
                {user && isFormOpen && !submission && (
                    <div className="mt-4 p-5 bg-slate-50 border border-slate-200 rounded-xl space-y-5">
                        <h3 className="text-xs font-bold text-slate-700 tracking-wider uppercase">Upload Assignment Deliverables</h3>

                        <div className="space-y-4 text-sm">
                            {/* File Upload Field Dropzone Style */}
                            <div>
                                <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">Select Digital Archive / Document</label>
                                <div className="relative border-2 border-dashed border-slate-300 rounded-xl bg-white p-4 hover:border-blue-500 transition-colors group text-center">
                                    <input
                                        type="file"
                                        onChange={(e) => setFile(e.target.files?.[0] || null)}
                                        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                                    />
                                    <div className="flex flex-col items-center justify-center pointer-events-none space-y-1.5 py-2">
                                        <UploadCloud className="h-7 w-7 text-slate-400 group-hover:text-blue-500 transition-colors" />
                                        <p className="text-xs font-medium text-slate-700">
                                            {file ? <span className="text-blue-600 font-semibold">{file.name}</span> : "Click to browse local files"}
                                        </p>
                                        <p className="text-[11px] text-slate-400">Standard formats accepted (PDF, ZIP, DOCX)</p>
                                    </div>
                                </div>
                            </div>

                            {/* Rename Field */}
                            <div>
                                <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">System File Renaming (Optional)</label>
                                <input
                                    type="text"
                                    placeholder="e.g., JaneDoe_Assignment1_v2.pdf"
                                    value={customName}
                                    onChange={(e) => setCustomName(e.target.value)}
                                    className="w-full bg-white border border-slate-300 px-3.5 py-2 rounded-lg text-slate-800 placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition text-sm shadow-sm"
                                />
                            </div>

                            {/* Feedback Field */}
                            <div>
                                <label className="block text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1.5">Student Notes for Evaluator (Optional)</label>
                                <textarea
                                    placeholder="Provide context or runtime execution instructions regarding your system file submission..."
                                    value={feedback}
                                    onChange={(e) => setFeedback(e.target.value)}
                                    className="w-full bg-white border border-slate-300 px-3.5 py-2 rounded-lg text-slate-800 placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition text-sm shadow-sm"
                                    rows={3}
                                />
                            </div>
                        </div>

                        {/* Action Controls */}
                        <div className="flex items-center gap-3 pt-2 border-t border-slate-200">
                            <button
                                onClick={handleSubmit}
                                disabled={submitting}
                                className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white text-xs font-bold uppercase tracking-wider px-5 py-2.5 rounded-lg transition shadow-sm flex items-center gap-1.5"
                            >
                                {submitting && <Loader2 className="h-3.5 w-3.5 animate-spin" />}
                                {submitting ? "Uploading Materials..." : "Finalize & Submit"}
                            </button>
                            <button
                                onClick={handleCancel}
                                disabled={submitting}
                                className="bg-white hover:bg-slate-100 text-slate-700 border border-slate-300 text-xs font-bold uppercase tracking-wider px-5 py-2.5 rounded-lg transition"
                            >
                                Dismiss
                            </button>
                        </div>
                    </div>
                )}
            </section>
        </div>
    );
}