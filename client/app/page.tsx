"use client"; // MUST be first line

import { BrowserRouter, Routes, Route } from "react-router-dom";
import LoginPage from "./Auth/loginpage";

export default function AppPage() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LoginPage />} />
      </Routes>
    </BrowserRouter>
  );
}
