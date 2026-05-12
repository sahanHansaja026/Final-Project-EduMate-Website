"use client";

import { usePathname } from "next/navigation";
import Navbar from "./Navbar";
import Footer from "./footer";
import ChatBot from "./chatbot";

type LayoutWrapperProps = {
  position: "top" | "bottom";
};

export default function LayoutWrapper({
  position,
}: LayoutWrapperProps): JSX.Element | null {
  const pathname = usePathname();

  const hideLayout = pathname.startsWith("/auth");

  if (hideLayout) return null;

  // TOP = Navbar
  if (position === "top") {
    return <Navbar />;
  }

  // BOTTOM = Footer + ChatBot
  return (
    <>
      <ChatBot />
      <Footer />
    </>
  );
}