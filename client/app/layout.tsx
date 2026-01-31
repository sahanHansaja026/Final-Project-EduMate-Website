// app/layout.tsx
import "./globals.css"
import { ReactNode } from "react"
import NavbarWrapper from "./components/NavbarWrapper"

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-gray-50">
        <NavbarWrapper />
        <main>{children}</main>
      </body>
    </html>
  )
}
