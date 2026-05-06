"use client";

import { useParams } from "next/navigation";

export default function Page() {
    const params = useParams();
    const id = params.id as string;

    return (
        <div>
            <h1>Quiz ID: {id}</h1>
        </div>
    );
}