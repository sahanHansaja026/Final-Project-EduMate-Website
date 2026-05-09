"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";

import {
    PlayCircle,
    ExternalLink,
    Calendar,
    Clock,
    Video as VideoIcon
} from "lucide-react";

import { API_BASE_URL } from "@/app/config/api";
import { getUser } from "@/app/services/authService";

import WeekContent from "@/app/components/WeekContent";

type Module = {
    module_id: number;
    user_id: number;
    name: string;
    description: string;
    skills?: string[];
    visibility?: string;
};

type Video = {
    id: number;

    module_id: number;

    title: string;
    description?: string;

    source_type: string;

    video_url?: string;
    thumbnail_url?: string;

    open_date?: string;
    close_date?: string;

    created_at?: string;
};

export default function CoursePage() {

    const params = useParams();
    const id = params?.id;

    // =========================
    // STATES
    // =========================

    const [authUser, setAuthUser] = useState<any>(null);

    const [profile, setProfile] = useState<any>(null);

    const [module, setModule] = useState<Module | null>(null);

    const [videos, setVideos] = useState<Video[]>([]);

    const [loading, setLoading] = useState(true);

    const [videoLoading, setVideoLoading] = useState(true);

    const [activeWeek, setActiveWeek] = useState<number>(1);

    const [showMore, setShowMore] = useState(false);

    // =========================
    // LOAD MODULE
    // =========================

    useEffect(() => {

        const fetchModule = async () => {

            try {

                const res = await fetch(
                    `${API_BASE_URL}/modules/${id}`
                );

                const data = await res.json();

                setModule(data);

            } catch (err) {

                console.error(err);

            } finally {

                setLoading(false);
            }
        };

        if (id) {
            fetchModule();
        }

    }, [id]);

    // =========================
    // LOAD VIDEOS
    // =========================

    useEffect(() => {

        const fetchVideos = async () => {

            try {

                const res = await fetch(
                    `${API_BASE_URL}/videos/module/${id}`
                );

                if (!res.ok) {
                    setVideos([]);
                    return;
                }

                const data = await res.json();

                setVideos(data);

            } catch (err) {

                console.error(err);

            } finally {

                setVideoLoading(false);
            }
        };

        if (id) {
            fetchVideos();
        }

    }, [id]);

    // =========================
    // LOAD AUTH USER
    // =========================

    useEffect(() => {

        const localUser = getUser();

        setAuthUser(localUser);

    }, []);

    // =========================
    // LOAD PROFILE
    // =========================

    useEffect(() => {

        const localUser = getUser();

        const fetchUserProfile = async () => {

            if (!localUser?.email) return;

            try {

                const res = await fetch(
                    `${API_BASE_URL}/profiles/by-email?email=${localUser.email}`
                );

                const data = await res.json();

                setProfile(data);

            } catch (err) {

                console.error(err);
            }
        };

        fetchUserProfile();

    }, []);

    // =========================
    // OWNER CHECK
    // =========================

    const isOwner =
        authUser &&
        module &&
        authUser.user_id === module.user_id;

    // =========================
    // LOADING
    // =========================

    if (loading) {

        return (
            <div className="flex items-center justify-center min-h-screen">

                <p className="text-gray-500">
                    Loading module...
                </p>

            </div>
        );
    }

    // =========================
    // MODULE NOT FOUND
    // =========================

    if (!module) {

        return (
            <div className="flex items-center justify-center min-h-screen">

                <p className="text-red-500">
                    Module not found
                </p>

            </div>
        );
    }

    return (

        <div className="flex flex-col lg:flex-row min-h-screen bg-gray-50">

            {/* ================= SIDEBAR ================= */}

            <aside className="w-full lg:w-72 bg-white border-b lg:border-r lg:border-b-0 
                lg:h-screen lg:sticky top-0 overflow-x-auto lg:overflow-y-auto">

                <div className="p-4 border-b">

                    <h2 className="text-xl font-bold">
                        📚 Course Content
                    </h2>

                    <p className="text-xs text-gray-500 mt-1">
                        Select a week to view content
                    </p>

                </div>

                <div className="p-3 flex lg:block gap-2 overflow-x-auto">

                    {[1, 2, 3, 4, 5].map((week) => (

                        <button
                            key={week}
                            onClick={() => setActiveWeek(week)}
                            className={`whitespace-nowrap lg:w-full text-left px-4 py-3 rounded-lg font-medium transition
                            
                            ${activeWeek === week
                                    ? "bg-blue-50 text-blue-600"
                                    : "hover:bg-gray-100"
                                }`}
                        >

                            Week {week}

                        </button>

                    ))}

                </div>

            </aside>

            {/* ================= MAIN CONTENT ================= */}

            <main className="flex-1 p-4 sm:p-6 lg:p-10 space-y-6 lg:space-y-8">

                {/* ================= MODULE HEADER ================= */}

                <div className="bg-white border rounded-lg">

                    <div className="border-b px-4 sm:px-6 py-4">

                        <h1 className="text-xl sm:text-2xl font-semibold text-gray-900">
                            {module.name}
                        </h1>

                    </div>

                    <div className="p-4 sm:p-6 overflow-x-auto">

                        <table className="min-w-full text-sm text-left">

                            <tbody>

                                <tr className="border-b">

                                    <th className="py-3 text-gray-500 w-48">
                                        Module ID
                                    </th>

                                    <td className="py-3 text-gray-800">
                                        {module.module_id}
                                    </td>

                                </tr>

                                <tr className="border-b">

                                    <th className="py-3 text-gray-500">
                                        Visibility
                                    </th>

                                    <td className="py-3 text-gray-800">
                                        {module.visibility}
                                    </td>

                                </tr>

                                <tr className="border-b">

                                    <th className="py-3 text-gray-500">
                                        Module owner
                                    </th>

                                    <td className="py-3 text-gray-800">

                                        {profile
                                            ? `${profile.firstName} ${profile.lastName} (${profile.email})`
                                            : "Loading..."}

                                    </td>

                                </tr>

                                <tr>

                                    <th className="py-3 text-gray-500">
                                        Status
                                    </th>

                                    <td className="py-3 text-gray-800">

                                        {module.visibility === "public"
                                            ? "Public Access"
                                            : "Restricted Access"}

                                    </td>

                                </tr>

                            </tbody>

                        </table>

                    </div>

                </div>

                {/* ================= DESCRIPTION ================= */}

                <div className="bg-white border rounded-lg">

                    <div className="border-b px-4 sm:px-6 py-4">

                        <h2 className="text-lg font-semibold text-gray-900">
                            Description
                        </h2>

                    </div>

                    <div className="p-4 sm:p-6">

                        <p className="text-gray-700 text-sm leading-7">

                            {showMore
                                ? module.description
                                : module.description.slice(0, 250) + "..."}

                        </p>

                        <button
                            onClick={() => setShowMore(!showMore)}
                            className="mt-4 text-sm underline"
                        >

                            {showMore
                                ? "Show less"
                                : "Show more"}

                        </button>

                    </div>

                </div>

                {/* ================= VIDEOS ================= */}

                {!videoLoading && videos.length > 0 && (

                    <div className="bg-white border rounded-lg">

                        <div className="border-b px-4 sm:px-6 py-4 flex items-center gap-2">

                            <VideoIcon className="w-5 h-5 text-blue-600" />

                            <h2 className="text-lg font-semibold text-gray-900">
                                Course Videos
                            </h2>

                        </div>

                        <div className="p-4 sm:p-6">

                            <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">

                                {videos.map((video) => (

                                    <div
                                        key={video.id}
                                        className="border rounded-xl overflow-hidden bg-white hover:shadow-lg transition"
                                    >

                                        {/* THUMBNAIL */}

                                        <div className="relative aspect-video bg-gray-100">

                                            {video.thumbnail_url ? (

                                                <img
                                                    src={`${API_BASE_URL}/${video.thumbnail_url}`}
                                                    alt={video.title}
                                                    className="w-full h-full object-cover"
                                                />

                                            ) : (

                                                <div className="w-full h-full flex items-center justify-center">

                                                    <VideoIcon className="w-10 h-10 text-gray-300" />

                                                </div>

                                            )}

                                            <div className="absolute inset-0 bg-black/20 flex items-center justify-center">

                                                <PlayCircle className="w-14 h-14 text-white drop-shadow-lg" />

                                            </div>

                                        </div>

                                        {/* CONTENT */}

                                        <div className="p-4 space-y-3">

                                            <div>

                                                <h3 className="font-semibold text-gray-900 line-clamp-2">
                                                    {video.title}
                                                </h3>

                                                <p className="text-sm text-gray-500 mt-1 line-clamp-3">
                                                    {video.description}
                                                </p>

                                            </div>

                                            {/* META */}

                                            <div className="space-y-2 text-xs text-gray-500">

                                                {video.open_date && (

                                                    <div className="flex items-center gap-2">

                                                        <Calendar className="w-4 h-4" />

                                                        <span>
                                                            Open: {video.open_date}
                                                        </span>

                                                    </div>

                                                )}

                                                {video.close_date && (

                                                    <div className="flex items-center gap-2">

                                                        <Clock className="w-4 h-4" />

                                                        <span>
                                                            Close: {video.close_date}
                                                        </span>

                                                    </div>

                                                )}

                                            </div>

                                            {/* ACTIONS */}

                                            <div className="pt-2">

                                                {video.source_type === "Upload" ? (

                                                    <video
                                                        controls
                                                        className="w-full rounded-lg"
                                                    >

                                                        <source
                                                            src={`${API_BASE_URL}/${video.video_url}`}
                                                        />

                                                    </video>

                                                ) : (

                                                    <a
                                                        href={video.video_url}
                                                        target="_blank"
                                                        className="inline-flex items-center gap-2 text-sm font-medium text-blue-600 hover:underline"
                                                    >

                                                        <ExternalLink className="w-4 h-4" />

                                                        Watch Video

                                                    </a>

                                                )}

                                            </div>

                                        </div>

                                    </div>

                                ))}

                            </div>

                        </div>

                    </div>

                )}

                {/* ================= WEEK CONTENT ================= */}

                <div className="bg-white border rounded-lg p-4 sm:p-6">

                    <h2 className="text-lg font-semibold text-gray-900 mb-4">
                        Weekly Content
                    </h2>

                    <WeekContent
                        weeks={5}
                        itemsPerWeek={1}
                        activeWeek={activeWeek}
                        currentUserId={authUser?.id}
                        moduleUserId={module?.user_id}
                        moduleId={module?.module_id}
                    />

                </div>

            </main>

        </div>
    );
}