"use client"

import { usePathname } from "next/navigation"
import Navbar from "./Navbar"

export default function NavbarWrapper() {
  const pathname = usePathname()
  const hideNavbar = pathname === "/auth/login" || pathname === "/auth/signuppage"

  if (hideNavbar) return null
  return <Navbar />
}
