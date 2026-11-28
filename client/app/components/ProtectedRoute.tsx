"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { getUser } from "@/app/services/authService";

export default function ProtectedRoute({
    children,
}: {
    children: React.ReactNode;
}) {
    const router = useRouter();
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        let cancelled = false;

        const checkAccess = async () => {
            const user = getUser();

            if (!user) {
                if (!cancelled) {
                    router.replace("/login"); // redirect if not logged in
                }
                return;
            }

            // Defer the state update out of the synchronous effect body.
            await Promise.resolve();
            if (!cancelled) {
                setLoading(false);
            }
        };

        checkAccess();

        return () => {
            cancelled = true;
        };
    }, [router]);

    if (loading) return null; // or a spinner

    return <>{children}</>;
}