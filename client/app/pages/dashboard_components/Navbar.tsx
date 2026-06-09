"use client";

import React, { useState, useEffect } from "react";
import { GraduationCap } from "lucide-react";

type Role = "student" | "owner" | "channel";

interface NavbarProps {
    currentRole: Role;
    onRoleChange: (role: Role) => void;
}

export default function Navbar({ currentRole, onRoleChange }: NavbarProps) {
    const [user, setUser] = useState<{ email: string } | null>(null);

    useEffect(() => {
        // This will connect directly to your auth system later
        setUser({ email: "sahan@university.edu" });
    }, []);

    return (
        <header className="border-b border-gray-200 bg-white sticky top-0 z-50 px-6 py-4 flex flex-col sm:flex-row justify-between items-center gap-4">
            {/* Brand Logo */}
            <div className="flex items-center gap-3">
                <GraduationCap className="h-7 w-7 text-gray-900" />
                <span className="text-lg font-black tracking-tight text-gray-900">LMS CORE</span>
            </div>

            {/* Dynamic Role Switcher (Simulated environment controller) */}
            <div className="flex bg-gray-100 p-1 rounded-lg border border-gray-200 text-xs">
                {(["student", "owner", "channel"] as const).map((r) => (
                    <button
                        key={r}
                        onClick={() => onRoleChange(r)}
                        className={`px-4 py-2 rounded-md font-bold tracking-wide uppercase transition-all ${currentRole === r
                                ? "bg-gray-900 text-white shadow-sm"
                                : "text-gray-500 hover:text-gray-900"
                            }`}
                    >
                        {r === "owner" ? "Module Owner" : r === "channel" ? "Channel Host" : r}
                    </button>
                ))}
            </div>

            {/* User Status Profile */}
            {user && (
                <div className="flex items-center gap-3">
                    <div className="text-right hidden sm:block">
                        <p className="text-sm font-bold text-gray-900">{user.email}</p>
                        <p className="text-[10px] font-mono font-medium text-gray-400 uppercase tracking-wider">Verified Account</p>
                    </div>
                    <div className="h-9 w-9 rounded-full bg-gray-900 text-white flex items-center justify-center font-black text-sm select-none">
                        {user.email[0].toUpperCase()}
                    </div>
                </div>
            )}
        </header>
    );
}