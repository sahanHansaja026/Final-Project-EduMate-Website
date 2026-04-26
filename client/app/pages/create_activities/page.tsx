"use client";

import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const modules = [
    {
        title: "Content Delivery",
        items: [
            "Upload lecture notes (PDF, DOC, slides)",
            "Add videos (YouTube, Vimeo, uploads)",
            "Add audio lessons or podcasts",
            "Provide reading materials or external links",
            "Organize content into structured sections"
        ]
    },
    {
        title: "Quizzes & Assessments",
        items: [
            "Create MCQ, true/false, short answer quizzes",
            "Timed quizzes and exams",
            "Question banks with randomization",
            "Auto and manual grading",
            "Attempt limitations",
            "Feedback and result review"
        ]
    },
    {
        title: "Assignments",
        items: [
            "Create assignment tasks",
            "File upload submissions",
            "Text-based submissions",
            "Deadlines and late submission rules",
            "Rubric-based grading",
            "Resubmission support"
        ]
    },
    {
        title: "Student Submissions",
        items: [
            "Upload assignments securely",
            "Drag and drop file upload",
            "Multi-file support",
            "Version tracking",
            "Submission status monitoring"
        ]
    },
    {
        title: "Communication",
        items: [
            "Discussion forums",
            "Q&A sections",
            "Instructor and student comments",
            "Announcements system",
            "Messaging support"
        ]
    },
    {
        title: "Live Learning",
        items: [
            "Live class integration",
            "Attendance tracking",
            "Live chat sessions",
            "Recorded lecture access"
        ]
    },
    {
        title: "Analytics",
        items: [
            "Student progress tracking",
            "Performance analytics",
            "Assignment reports",
            "Engagement metrics"
        ]
    },
    {
        title: "Learning Flow",
        items: [
            "Module unlocking system",
            "Prerequisite control",
            "Structured learning paths",
            "Conditional access rules"
        ]
    },
    {
        title: "Grading System",
        items: [
            "Centralized gradebook",
            "Weighted scoring system",
            "GPA calculation support",
            "Export grades",
            "Feedback management"
        ]
    },
    {
        title: "Resources",
        items: [
            "Central file repository",
            "Downloadable materials",
            "Shared learning resources",
            "Version control for files"
        ]
    },
    {
        title: "Group Activities",
        items: [
            "Group assignments",
            "Peer review system",
            "Collaborative submissions",
            "Group discussions"
        ]
    },
    {
        title: "Notifications",
        items: [
            "Deadline reminders",
            "Quiz notifications",
            "New content alerts",
            "Feedback notifications"
        ]
    },
    {
        title: "Instructor Tools",
        items: [
            "Create and manage modules",
            "Duplicate course structures",
            "Import and export courses",
            "Bulk upload content",
            "Publish and unpublish modules"
        ]
    },
    {
        title: "Advanced Features",
        items: [
            "AI-assisted quiz generation",
            "Automated coding evaluation",
            "Plagiarism detection",
            "Interactive coding environment",
            "Gamification system"
        ]
    }
];

export default function LMSModuleDashboard() {
    const [openIndex, setOpenIndex] = useState<number | null>(null);

    return (
        <div className="min-h-screen bg-white text-black">
            {/* Header */}
            <div className="border-b border-gray-200">
                <div className="max-w-7xl mx-auto px-6 py-5">
                    <h1 className="text-2xl font-semibold">Learning Management System</h1>
                    <p className="text-sm text-gray-900 mt-1">
                        Manage course modules, learning content, assessments, and student activity
                    </p>
                </div>
            </div>

            {/* Layout */}
            <div className="max-w-7xl mx-auto px-6 py-8 grid grid-cols-1 md:grid-cols-3 gap-6">

                {/* Sidebar */}
                <div className="md:col-span-1 space-y-2">
                    {modules.map((mod, index) => (
                        <Button
                            key={index}
                            variant="ghost"
                            className={`w-full justify-start text-left border border-gray-900 rounded-md px-3 py-2 hover:bg-gray-400 ${openIndex === index ? "bg-gray-100" : ""
                                }`}
                            onClick={() => setOpenIndex(index)}
                        >
                            {mod.title}
                        </Button>
                    ))}
                </div>

                {/* Content Panel */}
                <div className="md:col-span-2">
                    <Card className="border border-gray-900 shadow-sm rounded-lg">
                        <CardContent className="p-6">
                            {openIndex !== null ? (
                                <>
                                    <h2 className="text-xl font-semibold mb-4">
                                        {modules[openIndex].title}
                                    </h2>
                                    <ul className="space-y-3">
                                        {modules[openIndex].items.map((item, i) => (
                                            <li
                                                key={i}
                                                className="border border-gray-900 rounded-md p-3 text-sm hover:bg-gray-400"
                                            >
                                                {item}
                                            </li>
                                        ))}
                                    </ul>
                                </>
                            ) : (
                                <p className="text-gray-900 text-sm">
                                    Select a module from the left to view details
                                </p>
                            )}
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    );
}