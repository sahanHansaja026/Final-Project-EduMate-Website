"use client";

import { useEffect, useState } from "react";
import axios from "axios";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useParams } from "next/navigation";
import { API_BASE_URL } from "@/app/config/api";

export default function EditContentForm() {
    const params = useParams();

    const contentId = Array.isArray(params?.id)
        ? params.id[0]
        : params?.id;

    const [loading, setLoading] = useState(false);
    const [fetching, setFetching] = useState(true);

    const [title, setTitle] = useState("");
    const [week, setWeek] = useState<number>(1);
    const [description, setDescription] = useState("");
    const [externalUrl, setExternalUrl] = useState("");
    const [openDate, setOpenDate] = useState("");
    const [closeDate, setCloseDate] = useState("");
    const [allowDownload, setAllowDownload] = useState(false);

    // ✅ FETCH EXISTING DATA
    useEffect(() => {
        const fetchContent = async () => {
            if (!contentId) return;

            try {
                const res = await axios.get(
                    `${process.env.NEXT_PUBLIC_API_BASE_URL || `${API_BASE_URL}`}/contents/view/${contentId}`
                );

                const data = res.data;

                setTitle(data.title || "");
                setWeek(data.week || 1);
                setDescription(data.description || "");
                setExternalUrl(data.file_path || "");
                setAllowDownload(data.allow_download || false);

                setOpenDate(data.open_date ? data.open_date.split("T")[0] : "");
                setCloseDate(data.close_date ? data.close_date.split("T")[0] : "");

            } catch (err) {
                console.error(err);
                alert("Failed to load content");
            } finally {
                setFetching(false);
            }
        };

        fetchContent();
    }, [contentId]);

    // ✅ UPDATE
    const handleUpdate = async () => {
        setLoading(true);

        try {
            const formData = new FormData();

            formData.append("title", title);
            formData.append("week", String(week));
            formData.append("description", description || "");
            formData.append("external_url", externalUrl || "");
            formData.append("open_date", openDate || "");
            formData.append("close_date", closeDate || "");
            formData.append("allow_download", String(allowDownload));

            await axios.put(
                `${process.env.NEXT_PUBLIC_API_BASE_URL || `${API_BASE_URL}`}/contents/update/${contentId}`,
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                }
            );

            alert("Content updated successfully!");

        } catch (err) {
            console.error(err);
            alert("Update failed");
        } finally {
            setLoading(false);
        }
    };

    if (fetching) {
        return <p className="p-6">Loading content...</p>;
    }

    return (
        <Card className="rounded-2xl shadow-sm border">
            <CardContent className="p-6 space-y-5">

                <h3 className="text-lg font-semibold">
                    Edit Content
                </h3>

                <p className="text-sm text-gray-500">
                    Content ID: {contentId}
                </p>

                {/* TITLE */}
                <input
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    className="w-full border rounded-lg px-3 py-2"
                    placeholder="Title"
                />

                {/* WEEK */}
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

                {/* DESCRIPTION */}
                <textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    className="w-full border rounded-lg px-3 py-2 h-28"
                />

                {/* URL */}
                <input
                    value={externalUrl}
                    onChange={(e) => setExternalUrl(e.target.value)}
                    className="w-full border rounded-lg px-3 py-2"
                    placeholder="External URL"
                />

                {/* DATES */}
                <div className="grid md:grid-cols-2 gap-4">

                    <input
                        type="date"
                        value={openDate}
                        onChange={(e) => setOpenDate(e.target.value)}
                        className="w-full border rounded-lg px-3 py-2"
                    />

                    <input
                        type="date"
                        value={closeDate}
                        onChange={(e) => setCloseDate(e.target.value)}
                        className="w-full border rounded-lg px-3 py-2"
                    />

                </div>

                {/* DOWNLOAD */}
                <label className="flex items-center gap-2 text-sm">
                    <input
                        type="checkbox"
                        checked={allowDownload}
                        onChange={() => setAllowDownload(!allowDownload)}
                    />
                    Allow download
                </label>

                {/* ACTION */}
                <div className="flex justify-end">
                    <Button onClick={handleUpdate} disabled={loading}>
                        {loading ? "Updating..." : "Update Content"}
                    </Button>
                </div>

            </CardContent>
        </Card>
    );
}