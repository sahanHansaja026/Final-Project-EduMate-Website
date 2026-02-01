import "./globals.css";
import { ReactNode } from "react";
import LayoutWrapper from "./components/LayoutWrapper";

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col bg-gray-50">
        {/* Top */}
        <LayoutWrapper position="top" />

        {/* Page content grows */}
        <main className="flex-1">
          {children}
        </main>

        {/* Bottom */}
        <LayoutWrapper position="bottom" />
      </body>
    </html>
  );
}
