"use client";

import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function AddContentForm() {
    const [allowDownload, setAllowDownload] = useState(true);
    const [week, setWeek] = useState(1);

    return (
        <Card className="rounded-2xl shadow-sm">
            <CardContent className="p-6 space-y-5">
                <h3 className="text-lg font-semibold">Add New Content</h3>

                {/* Title */}
                <input
                    type="text"
                    placeholder="Title"
                    className="w-full border rounded-lg px-3 py-2"
                />

                {/* Week */}
                <div>
                    <label className="text-sm">Week</label>
                    <select
                        value={week}
                        onChange={(e) => setWeek(Number(e.target.value))}
                        className="w-full border rounded-lg px-3 py-2"
                    >
                        {Array.from({ length: 20 }, (_, i) => (
                            <option key={i + 1} value={i + 1}>
                                Week {i + 1}
                            </option>
                        ))}
                    </select>
                </div>

                {/* Description */}
                <textarea
                    placeholder="Description"
                    className="w-full border rounded-lg px-3 py-2"
                />

                {/* Upload / URL */}
                <div className="space-y-3">
                    <div className="border-2 border-dashed rounded-xl p-5 text-center">
                        <p className="text-sm text-muted-foreground">
                            Upload file or paste link
                        </p>
                        <Button className="mt-3">Upload</Button>
                    </div>

                    <input
                        type="text"
                        placeholder="Or paste external URL (YouTube, article, etc.)"
                        className="w-full border rounded-lg px-3 py-2"
                    />
                </div>

                {/* Dates */}
                <div className="grid md:grid-cols-2 gap-4">
                    <div>
                        <label className="text-sm">Open Date</label>
                        <input type="date" className="w-full border rounded-lg px-3 py-2" />
                    </div>

                    <div>
                        <label className="text-sm">Close Date</label>
                        <input type="date" className="w-full border rounded-lg px-3 py-2" />
                    </div>
                </div>

                {/* Allow Download */}
                <label className="flex items-center gap-2">
                    <input
                        type="checkbox"
                        checked={allowDownload}
                        onChange={() => setAllowDownload(!allowDownload)}
                    />
                    Allow students to download this content
                </label>

                {/* Actions */}
                <div className="flex justify-end gap-3">
                    <Button variant="outline">Cancel</Button>
                    <Button>Save Content</Button>
                </div>
            </CardContent>
        </Card>
    );
}