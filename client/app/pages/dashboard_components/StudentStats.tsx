import React from "react";
import { BookOpen, TrendingUp, CheckCircle, BarChart3, Layers } from "lucide-react";

export default function StudentStats() {
    // Mock data structural setup - ready for an array fetch injection
    const studentModules = [
        { id: 1, name: "Advanced Machine Learning & Classification", score: 88, progress: 75 },
        { id: 2, name: "Enterprise Microservices with FastAPI", score: 94, progress: 90 },
    ];

    const averageScore = Math.round(studentModules.reduce((acc, m) => acc + m.score, 0) / studentModules.length);
    const averageProgress = Math.round(studentModules.reduce((acc, m) => acc + m.progress, 0) / studentModules.length);

    return (
        <div className="space-y-8">
            {/* Metrics Row */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="border border-gray-200 rounded-xl p-6 bg-white flex items-center justify-between">
                    <div>
                        <p className="text-xs font-bold text-gray-400 uppercase tracking-wider">Enrolled Modules</p>
                        <p className="text-3xl font-black mt-1 text-gray-900">{studentModules.length}</p>
                    </div>
                    <BookOpen className="h-8 w-8 text-gray-300" />
                </div>

                <div className="border border-gray-200 rounded-xl p-6 bg-white flex items-center justify-between">
                    <div>
                        <p className="text-xs font-bold text-gray-400 uppercase tracking-wider">Grade Average</p>
                        <p className="text-3xl font-black mt-1 text-gray-900">{averageScore}%</p>
                    </div>
                    <TrendingUp className="h-8 w-8 text-gray-300" />
                </div>

                <div className="border border-gray-200 rounded-xl p-6 bg-white flex items-center justify-between">
                    <div>
                        <p className="text-xs font-bold text-gray-400 uppercase tracking-wider">Syllabus Completion</p>
                        <p className="text-3xl font-black mt-1 text-gray-900">{averageProgress}%</p>
                    </div>
                    <CheckCircle className="h-8 w-8 text-gray-300" />
                </div>
            </div>

            {/* Custom Bar Graphs Section */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                {/* Score Breakdown Chart */}
                <div className="border border-gray-200 rounded-xl p-6 bg-white">
                    <div className="flex items-center gap-2 mb-6 border-b border-gray-100 pb-4">
                        <BarChart3 className="h-5 w-5 text-gray-900" />
                        <h4 className="font-bold text-gray-900">Module Score Analysis</h4>
                    </div>
                    <div className="space-y-6">
                        {studentModules.map((mod) => (
                            <div key={mod.id} className="space-y-2">
                                <div className="flex justify-between text-xs font-medium">
                                    <span className="text-gray-700 truncate max-w-[85%]">{mod.name}</span>
                                    <span className="font-bold text-gray-900">{mod.score}%</span>
                                </div>
                                <div className="w-full bg-gray-100 rounded-full h-3">
                                    <div className="bg-gray-900 h-3 rounded-full transition-all duration-500" style={{ width: `${mod.score}%` }} />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                {/* System Progress Monitor */}
                <div className="border border-gray-200 rounded-xl p-6 bg-white">
                    <div className="flex items-center gap-2 mb-6 border-b border-gray-100 pb-4">
                        <Layers className="h-5 w-5 text-gray-900" />
                        <h4 className="font-bold text-gray-900">Syllabus Milestones</h4>
                    </div>
                    <div className="space-y-6">
                        {studentModules.map((mod) => (
                            <div key={mod.id} className="space-y-2">
                                <div className="flex justify-between text-xs font-medium">
                                    <span className="text-gray-700 truncate max-w-[85%]">{mod.name}</span>
                                    <span className="text-gray-400 font-mono">{mod.progress}% complete</span>
                                </div>
                                <div className="w-full bg-gray-100 rounded-full h-1.5">
                                    <div className="bg-gray-400 h-1.5 rounded-full transition-all duration-500" style={{ width: `${mod.progress}%` }} />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}