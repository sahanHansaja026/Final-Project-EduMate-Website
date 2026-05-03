"use client";

import { useState } from "react";
import WeekItemInfo from "./WeekItemInfo";

type WeekContentProps = {
    weeks?: number;
    itemsPerWeek?: number;
    activeWeek: number;
    moduleId: number | string;
    currentUserId?: number | string;
    moduleUserId?: number | string;
};

export default function WeekContent({
    weeks = 5,
    itemsPerWeek = 0,
    activeWeek,
    currentUserId,
    moduleUserId,
    moduleId,
}: WeekContentProps) {
    const [activeItem, setActiveItem] = useState<string | null>(null);

    const [doneItems, setDoneItems] = useState<Record<string, boolean>>({});

    const isOwner =
        currentUserId !== undefined &&
        moduleUserId !== undefined &&
        Number(currentUserId) === Number(moduleUserId);

    const toggleDone = (key: string) => {
        setDoneItems((prev) => ({
            ...prev,
            [key]: !prev[key],
        }));
    };

    return (
        <div className="space-y-6">


            {/* WEEK CONTENT */}
            {Array.from({ length: weeks }, (_, w) => {
                const weekNumber = w + 1;

                if (weekNumber !== activeWeek) return null;

                return (
                    <div key={w}>
                        <hr className="mb-3" />

                        

                        {isOwner ? (
                            <div className="space-y-2">
                                {Array.from({ length: itemsPerWeek }, (_, i) => {
                                    const key = `week-${w}-item-${i}`;
                                    const isDone = doneItems[key];

                                    return (
                                        <div key={key} className="space-y-2">

                                            {/* NEW COMPONENT HERE */}
                                            <WeekItemInfo moduleId={String(moduleId)} />
                                            <div className="flex items-center justify-between border rounded-md px-3 py-2">

                                                <a href={`/pages/create_activities/${moduleId}`}>
                                                    <button
                                                        onClick={() => setActiveItem(key)}
                                                        className={`px-4 py-2 rounded-md text-sm border transition
                            ${activeItem === key
                                                                ? "bg-blue-600 text-white"
                                                                : "bg-white hover:bg-gray-100"
                                                            }`}
                                                    >
                                                        Create
                                                    </button>
                                                </a>

                                                <button
                                                    onClick={() => toggleDone(key)}
                                                    className={`px-3 py-1 text-xs rounded-full border transition
                        ${isDone
                                                            ? "bg-green-500 text-white"
                                                            : "bg-gray-100 text-gray-600 hover:bg-gray-200"
                                                        }`}
                                                >
                                                    {isDone ? "Done" : "Mark as Done"}
                                                </button>

                                            </div>
                                        </div>
                                    );
                                })}
                            </div>
                        ) : (
                            <p className="text-sm text-gray-400">
                                You don’t have permission to view this content
                            </p>
                        )}

                        <hr className="mt-3" />
                    </div>
                );
            })}
        </div>
    );
}