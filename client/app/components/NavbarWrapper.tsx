"use client";

import { usePathname } from "next/navigation";
import Navbar from "./Navbar";
import Footer from "./footer";

export default function NavbarWrapper(): JSX.Element | null {
  const pathname = usePathname();

  const hideLayout =
    pathname === "/auth/login" ||
    pathname === "/auth/signuppage";

  if (hideLayout) return null;

  return (
    <>
      <Navbar />
      <Footer />
    </>
  );
}
