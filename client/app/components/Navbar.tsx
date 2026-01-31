"use client";

import React, { useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

// ---------------- Confirm Modal Component ----------------
interface ConfirmModalProps {
  message: string;
  onConfirm: () => void;
  onCancel: () => void;
}

const ConfirmModal: React.FC<ConfirmModalProps> = ({
  message,
  onConfirm,
  onCancel,
}) => {
  return (
    <div className="fixed inset-0 flex items-center justify-center bg-gray-500 bg-opacity-50 z-50">
      <div className="bg-white rounded-xl p-6 w-80 text-center shadow-lg animate-fadeIn">
        <p className="text-gray-800 text-lg">{message}</p>
        <div className="mt-6 flex justify-around gap-4">
          <button
            onClick={onConfirm}
            className="px-6 py-2 rounded-full bg-green-500 text-white hover:bg-green-600 transition"
          >
            Yes
          </button>
          <button
            onClick={onCancel}
            className="px-6 py-2 rounded-full bg-red-500 text-white hover:bg-red-600 transition"
          >
            No
          </button>
        </div>
      </div>
    </div>
  );
};

// ---------------- Navbar Component ----------------
const Navbar: React.FC = () => {
  const [open, setOpen] = useState<boolean>(false);
  const [showModal, setShowModal] = useState(false);
  const pathname = usePathname();
  const router = useRouter();

  // Check active link
  const isActive = (href: string) => pathname === href;

  // Handle Login click
  const handleLoginClick = (e: React.MouseEvent) => {
    e.preventDefault();
    setShowModal(true);
  };

  const handleConfirm = () => {
    setShowModal(false);
    router.push("/auth/login");
  };

  const handleCancel = () => {
    setShowModal(false);
  };

  return (
    <>
      <nav className="relative flex items-center justify-between px-6 md:px-16 lg:px-24 xl:px-32 py-4 border-b border-gray-300 bg-white">
        {/* Logo */}
        <Link href="/" className="flex items-center">
          <svg width="120" height="32" viewBox="0 0 157 40" fill="none">
            {/* SVG paths unchanged */}
          </svg>
        </Link>

        {/* Desktop Menu */}
        <div className="hidden sm:flex items-center gap-8">
          {[
            { href: "/pages/home", label: "Home" },
            { href: "/about", label: "About" },
            { href: "/contact", label: "Contact" },
          ].map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className={`hover:text-indigo-500 ${
                isActive(link.href) ? "border-b-2 border-indigo-500" : ""
              }`}
            >
              {link.label}
            </Link>
          ))}

          {/* Search */}
          <div className="hidden lg:flex items-center gap-2 border border-gray-300 px-3 rounded-full">
            <input
              type="text"
              placeholder="Search products"
              className="py-1.5 bg-transparent outline-none text-sm"
            />
            🔍
          </div>

          {/* Cart */}
          <div className="relative cursor-pointer">
            🛒
            <span className="absolute -top-2 -right-3 text-xs text-white bg-indigo-500 w-[18px] h-[18px] rounded-full flex items-center justify-center">
              3
            </span>
          </div>

          {/* Login Button */}
          <button
            onClick={handleLoginClick}
            className={`px-8 py-2 rounded-full text-white ${
              isActive("/auth/login")
                ? "bg-indigo-600"
                : "bg-indigo-500 hover:bg-indigo-600"
            }`}
          >
            Login
          </button>
        </div>

        {/* Mobile Menu Button */}
        <button
          aria-label="Toggle Menu"
          onClick={() => setOpen(!open)}
          className="sm:hidden"
        >
          {open ? "✖" : "☰"}
        </button>

        {/* Mobile Menu */}
        <div
          className={`${
            open ? "flex" : "hidden"
          } absolute top-[64px] left-0 w-full bg-white shadow-md flex-col gap-4 px-6 py-6 sm:hidden`}
        >
          {[
            { href: "/pages/home", label: "Home" },
            { href: "/about", label: "About" },
            { href: "/contact", label: "Contact" },
          ].map((link) => (
            <Link
              key={link.href}
              href={link.href}
              onClick={() => setOpen(false)}
              className={`${
                isActive(link.href) ? "border-b-2 border-indigo-500" : ""
              }`}
            >
              {link.label}
            </Link>
          ))}

          {/* Mobile Login */}
          <button
            onClick={() => {
              setOpen(false);
              handleLoginClick;
            }}
            className={`mt-2 px-6 py-2 rounded-full text-white text-center ${
              isActive("/auth/login")
                ? "bg-indigo-600"
                : "bg-indigo-500 hover:bg-indigo-600"
            }`}
          >
            Login
          </button>
        </div>
      </nav>

      {/* Confirm Modal */}
      {showModal && (
        <ConfirmModal
          message="Do you want to go to the Login page?"
          onConfirm={handleConfirm}
          onCancel={handleCancel}
        />
      )}
    </>
  );
};

export default Navbar;
