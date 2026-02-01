"use client";

import { usePathname } from "next/navigation";
import Navbar from "./Navbar";
import Footer from "./footer";

type LayoutWrapperProps = {
  position: "top" | "bottom";
};

export default function LayoutWrapper({
  position,
}: LayoutWrapperProps): JSX.Element | null {
  const pathname = usePathname();

  const hideLayout = pathname.startsWith("/auth");

  if (hideLayout) return null;

  if (position === "top") {
    return <Navbar />;
  }

  return <Footer />;
}
